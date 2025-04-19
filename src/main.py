import asyncio

import discord

import config
from utils.async_interrupt import create_interrupt_future


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def close(self):
        await super().close()
        print("Closed up shop")


intents = discord.Intents.default()


async def main():
    until = create_interrupt_future()
    async with MyClient(intents=intents) as client:
        connect_future = asyncio.create_task(client.start(config.discord_app_bot_token))
        await until
    await connect_future


if __name__ == "__main__":
    asyncio.run(main())
