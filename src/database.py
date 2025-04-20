from discord import User

from utils.jellycat_api import Jellycat

subscribers: set[User] = set()
unavailable_jellycats: set[Jellycat] = set()

__all__ = ("subscribers", "unavailable_jellycats",)
