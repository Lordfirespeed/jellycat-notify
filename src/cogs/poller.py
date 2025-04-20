import discord
from discord import app_commands, InteractionResponse
from discord.ext import commands, tasks

import database


class JellycatPoller(commands.Cog, name="Jellycat Poller"):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self) -> None:
        self.poll.start()

    async def cog_unload(self) -> None:
        self.poll.cancel()

    async def check_for_new_jellycat_stock(self) -> None:
        print("hehe")

    @tasks.loop(hours=1)
    async def poll(self) -> None:
        await self.check_for_new_jellycat_stock()

    @poll.before_loop
    async def on_start(self):
        await self.bot.wait_until_ready()


__all__ = ("JellycatPoller",)
