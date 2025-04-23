from piccolo.table import Table
from piccolo.columns import Integer, Boolean, Timestamp
from piccolo.columns.defaults.timestamp import TimestampNow


class Subscriber(Table):
    discord_user_id = Integer(primary_key=True)


# it's possible I want a multi-column index here, but they aren't properly supported by Piccolo, so meh
class JellycatRecord(Table):
    jellycat_uid = Integer(index=True)
    is_available = Boolean()
    timestamp = Timestamp(index=True, default=TimestampNow())


__all__ = (
    "Subscriber",
    "JellycatRecord",
)
