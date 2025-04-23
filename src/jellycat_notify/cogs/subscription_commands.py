import sqlite3

import discord
from discord import app_commands, InteractionResponse
from discord.ext import commands

from jellycat_notify.tables import Subscriber


class SubscriptionCommands(commands.Cog, name="Subscribe Commands"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="subscribe")
    async def subscribe(self, interaction: discord.Interaction):
        """Subscribe to jellycat stock notifications.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object.
        """
        response: InteractionResponse = interaction.response

        try:
            await Subscriber.insert(
                Subscriber(discord_user_id=interaction.user.id),
            )
        except sqlite3.IntegrityError as e:
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_PRIMARYKEY:
                await response.send_message(content="You are already subscribed :heart:")
            raise
        await response.send_message(content="you have subscribed! :heart:")

    @app_commands.command(name="unsubscribe")
    async def unsubscribe(self, interaction: discord.Interaction):
        """Unsubscribe from jellycat stock notifications.

        :param interaction:
        :return:
        """
        response: InteractionResponse = interaction.response

        deleted = await Subscriber.delete() \
            .where(Subscriber.discord_user_id == interaction.user.id) \
            .returning(Subscriber.discord_user_id)

        if len(deleted) == 0:
            await response.send_message(content="You aren't subscribed :confused:")
            return

        await response.send_message(content="you have unsubscribed :broken_heart:")


__all__ = ("SubscriptionCommands",)
