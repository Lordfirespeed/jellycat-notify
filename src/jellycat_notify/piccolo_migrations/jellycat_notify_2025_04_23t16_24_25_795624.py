from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Boolean
from piccolo.columns.column_types import Integer
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.columns.indexes import IndexMethod


ID = "2025-04-23T16:24:25:795624"
VERSION = "1.24.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="jellycat_notify", description=DESCRIPTION
    )

    manager.add_table(
        class_name="Subscriber", tablename="subscriber", schema=None, columns=None
    )

    manager.add_table(
        class_name="JellycatRecord",
        tablename="jellycat_record",
        schema=None,
        columns=None,
    )

    manager.add_column(
        table_class_name="Subscriber",
        tablename="subscriber",
        column_name="discord_user_id",
        db_column_name="discord_user_id",
        column_class_name="Integer",
        column_class=Integer,
        params={
            "default": 0,
            "null": False,
            "primary_key": True,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="JellycatRecord",
        tablename="jellycat_record",
        column_name="jellycat_uid",
        db_column_name="jellycat_uid",
        column_class_name="Integer",
        column_class=Integer,
        params={
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": True,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="JellycatRecord",
        tablename="jellycat_record",
        column_name="is_available",
        db_column_name="is_available",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="JellycatRecord",
        tablename="jellycat_record",
        column_name="timestamp",
        db_column_name="timestamp",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": TimestampNow(),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": True,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )



    return manager
