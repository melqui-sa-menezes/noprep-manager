import os


class DatabaseRouter:
    """
    A router to control all database operations on models in the
    auth application.
    https://docs.djangoproject.com/en/5.0/topics/db/multi-db/#database-routers
    """

    def __init__(self) -> None:
        self.database_url = os.environ.get("DATABASE_URL")
        self.database_read_url = os.environ.get("DATABASE_READ_URL")

    def db_for_read(self, model, **hints):
        if self.database_url == self.database_read_url:
            return "default"
        return "default_read"

    def db_for_write(self, model, **hints):
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
