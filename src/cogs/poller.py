import asyncio

import aiohttp
from contextlib import AsyncExitStack
from discord.ext import commands, tasks

import database

from utils.jellycat_api import fetch_all_jellycats, ProductStatus, Jellycat, fetch_one_jellycat


class JellycatPoller(commands.Cog, name="Jellycat Poller"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        self.poll.start()

    async def cog_unload(self) -> None:
        self.poll.cancel()

    async def notify_jellycat_in_stock(self, jellycat: Jellycat) -> None:
        notification_body = f"Jellycat stock alert - [{jellycat.name}]({jellycat.url}) is available for purchase!"

        async def deliver_notification(subscriber_user_id: int) -> None:
            nonlocal notification_body
            user = self.bot.get_user(subscriber_user_id) or await self.bot.fetch_user(subscriber_user_id)
            await user.send(content=notification_body)

        async with asyncio.TaskGroup() as task_group:
            for subscriber_user_id in database.subscriber_user_ids:
                task_group.create_task(deliver_notification(subscriber_user_id))

    async def check_for_new_jellycat_stock(self) -> None:
        async with AsyncExitStack() as stack:
            session = await stack.enter_async_context(aiohttp.ClientSession())
            task_group: asyncio.TaskGroup = await stack.enter_async_context(asyncio.TaskGroup())

            async for jellycat in fetch_all_jellycats(session):
                if jellycat.uid in database.unavailable_jellycat_uids and jellycat.product_status == ProductStatus.Live and jellycat.in_stock:
                    database.unavailable_jellycat_uids.discard(jellycat.uid)
                    task_group.create_task(self.notify_jellycat_in_stock(jellycat))

                if jellycat.in_stock == False or jellycat.product_status != ProductStatus.Live:
                    database.unavailable_jellycat_uids.add(jellycat.uid)
                    continue

    @tasks.loop(minutes=1)
    async def poll(self) -> None:
        await self.check_for_new_jellycat_stock()

    @poll.before_loop
    async def on_start(self):
        await self.bot.wait_until_ready()


__all__ = ("JellycatPoller",)
