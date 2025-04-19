import os

from dotenv import dotenv_values


config = {
    **os.environ,
    **dotenv_values(".env"),
    **dotenv_values(".env.local"),
}


discord_app_bot_token = config.get("DISCORD_APP_BOT_TOKEN")
assert isinstance(discord_app_bot_token, str) and not discord_app_bot_token.isspace()


__all__ = (
    "discord_app_bot_token",
)
