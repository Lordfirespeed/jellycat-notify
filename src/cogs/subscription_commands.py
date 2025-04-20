import discord
from discord import app_commands, InteractionResponse
from discord.ext import commands

import database


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
        if interaction.user.id in database.subscriber_user_ids:
            await response.send_message(content="You are already subscribed :heart:")
            return
        database.subscriber_user_ids.add(interaction.user.id)
        await response.send_message(content="you have subscribed! :heart:")

    @app_commands.command(name="unsubscribe")
    async def unsubscribe(self, interaction: discord.Interaction):
        """Unsubscribe from jellycat stock notifications.

        :param interaction:
        :return:
        """
        response: InteractionResponse = interaction.response
        if not interaction.user.id in database.subscriber_user_ids:
            await response.send_message(content="You aren't subscribed :confused:")
            return
        database.subscriber_user_ids.discard(interaction.user.id)
        await response.send_message(content="you have unsubscribed :broken_heart:")


__all__ = ("SubscriptionCommands",)
