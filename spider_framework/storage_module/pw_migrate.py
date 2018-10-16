from . import items
from peewee_migrate import Router


def run(path):
    items.db.connect()

    router = Router(items.db, ignore="basemodel", migrate_dir=path, migrate_table='toolsmigrate')

    router.create(auto=items)
    router.run()

    items.db.close()
