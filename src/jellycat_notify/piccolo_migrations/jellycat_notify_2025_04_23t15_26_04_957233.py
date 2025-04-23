from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2025-04-23T15:26:04:957233"
VERSION = "1.24.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="", description=DESCRIPTION
    )

    def run():
        print(f"running {ID}")

    manager.add_raw(run)

    return manager
