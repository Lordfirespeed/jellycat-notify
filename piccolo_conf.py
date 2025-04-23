from piccolo.conf.apps import AppRegistry
from piccolo.engine.sqlite import SQLiteEngine

from definitions import project_data_directory

DB = SQLiteEngine(
    path=(project_data_directory / "database.db"),
)


# A list of paths to piccolo apps
# e.g. ['blog.piccolo_app']
APP_REGISTRY = AppRegistry(apps=["jellycat_notify.piccolo_app"])
