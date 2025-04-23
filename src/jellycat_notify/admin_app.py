import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config
from piccolo_admin.endpoints import create_admin

from jellycat_notify.piccolo_app import APP_CONFIG

admin = create_admin(APP_CONFIG.table_classes, site_name="Jellycat Notify Admin")


class CustomConfig(Config):
    use_reloader = True
    accesslog = "-"


async def main():
    await serve(admin, CustomConfig())


if __name__ == "__main__":
    asyncio.run(main())
