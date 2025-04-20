import asyncio
from typing import ClassVar, Type

import discord
from discord.ext import commands

import config
from cogs.poller import JellycatPoller
from cogs.subscription_commands import SubscriptionCommands
from cogs.ping_command import PingCommand
from utils.async_interrupt import create_interrupt_future


class MyClient(commands.Bot):
    cog_types: ClassVar[list[Type[commands.Cog]]] = [
        PingCommand,
        SubscriptionCommands,
        JellycatPoller,
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def setup_hook(self) -> None:
        for cog_type in self.cog_types:
            cog = cog_type(self)
            await self.add_cog(cog)
        await self.tree.sync()

    async def close(self):
        await super().close()
        print("Closed up shop")


intents = discord.Intents.default()


async def main():
    until = create_interrupt_future()
    async with MyClient(command_prefix=None, intents=intents) as client:
        connect_future = asyncio.create_task(client.start(config.discord_app_bot_token))
        await until
    await connect_future


if __name__ == "__main__":
    asyncio.run(main())
