import asyncio

import aiohttp
from contextlib import AsyncExitStack
from discord.ext import commands, tasks

import database

from utils.jellycat_api import fetch_all_jellycats, ProductStatus, Jellycat, fetch_one_jellycat


class JellycatPoller(commands.Cog, name="Jellycat Poller"):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self) -> None:
        self.poll.start()

    async def cog_unload(self) -> None:
        self.poll.cancel()

    async def notify_jellycat_in_stock(self, jellycat: Jellycat) -> None:
        async with asyncio.TaskGroup as task_group:
            for subscriber in database.subscribers:
                task_group.create_task(subscriber.send(content=f"Jellycat stock alert - [{jellycat.name}]({jellycat.url}) is available for purchase!"))

    async def check_for_new_jellycat_stock(self) -> None:
        async with AsyncExitStack() as stack:
            session = await stack.enter_async_context(aiohttp.ClientSession())
            task_group: asyncio.TaskGroup = await stack.enter_async_context(asyncio.TaskGroup())

            async for jellycat in fetch_all_jellycats(session):
                if jellycat in database.unavailable_jellycats and jellycat.product_status == ProductStatus.Live and jellycat.in_stock:
                    database.unavailable_jellycats.discard(jellycat)
                    task_group.create_task(self.notify_jellycat_in_stock(jellycat))

                if jellycat.in_stock == False or jellycat.product_status != ProductStatus.Live:
                    database.unavailable_jellycats.add(jellycat)
                    continue

    @tasks.loop(minutes=1)
    async def poll(self) -> None:
        await self.check_for_new_jellycat_stock()
        print(database.unavailable_jellycats)

    @poll.before_loop
    async def on_start(self):
        await self.bot.wait_until_ready()


__all__ = ("JellycatPoller",)
