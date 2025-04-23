from piccolo.table import Table
from piccolo.columns import Integer


class Subscriber(Table):
    discord_user_id = Integer(primary_key=True)


class JellycatRecord(Table):
    uid = Integer(primary_key=True)


__all__ = (
    "Subscriber",
    "JellycatRecord",
)
