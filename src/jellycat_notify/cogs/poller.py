import asyncio

import aiohttp
from contextlib import AsyncExitStack
from discord.ext import commands, tasks

from jellycat_notify.tables import Subscriber, JellycatRecord
from jellycat_notify.utils.jellycat_api import fetch_all_jellycats, Jellycat


class JellycatPoller(commands.Cog, name="Jellycat Poller"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        self.poll.start()

    async def cog_unload(self) -> None:
        self.poll.cancel()

    async def notify_jellycats_in_stock(self, jellycats: list[Jellycat]) -> None:
        notification_body_lines = [
            "# Stock alert!",
            "These fellas are available for purchase:",
            *(f"- [{jellycat.name}]({jellycat.url})" for jellycat in jellycats),
        ]
        notification_body = "\n".join(notification_body_lines)

        async def deliver_notification(subscriber_user_id: int) -> None:
            nonlocal notification_body
            user = self.bot.get_user(subscriber_user_id) or await self.bot.fetch_user(subscriber_user_id)
            await user.send(content=notification_body)

        async def deliver_notification_batch(subscribers: list[Subscriber]) -> None:
            async with asyncio.TaskGroup() as task_group:
                for subscriber in subscribers:
                    task_group.create_task(deliver_notification(subscriber.discord_user_id))

        async with await Subscriber.objects().batch(batch_size=100) as batcher:
            batch: list[Subscriber]
            async for batch in batcher:
                await deliver_notification_batch(batch)

    async def insert_jellycat_record(self, jellycat: Jellycat) -> None:
        await JellycatRecord.insert(
            JellycatRecord(
                jellycat_uid=jellycat.uid,
                is_available=jellycat.is_available,
            )
        )

    async def check_for_new_jellycat_stock(self) -> None:
        jellycats_newly_in_stock = []

        async with AsyncExitStack() as stack:
            session = await stack.enter_async_context(aiohttp.ClientSession())

            async for jellycat in fetch_all_jellycats(session):
                most_recent_records = await JellycatRecord.objects() \
                    .where(JellycatRecord.jellycat_uid == jellycat.uid) \
                    .order_by(JellycatRecord.timestamp, ascending=False) \
                    .limit(1)
                if len(most_recent_records) == 0:
                    await self.insert_jellycat_record(jellycat)
                    continue
                most_recent_record = most_recent_records[0]

                if (most_recent_record.is_available == False) and jellycat.is_available:
                    jellycats_newly_in_stock.append(jellycat)

                if most_recent_record.is_available != jellycat.is_available:
                    await self.insert_jellycat_record(jellycat)

        if len(jellycats_newly_in_stock) == 0:
            return

        await self.notify_jellycats_in_stock(jellycats_newly_in_stock)

    @tasks.loop(minutes=1)
    async def poll(self) -> None:
        await self.check_for_new_jellycat_stock()

    @poll.before_loop
    async def on_start(self):
        await self.bot.wait_until_ready()


__all__ = ("JellycatPoller",)
