'''
数据库跟踪模块
'''

from . import db_items_module
from peewee_migrate import Router


def run(path):
    db_items_module.db.connect()

    # migrate_table: 迁移表的名称
    router = Router(db_items_module.db, ignore="basemodel", migrate_dir=path, migrate_table='toolsmigrate')

    router.create(auto=db_items_module)
    router.run()

    db_items_module.db.close()
