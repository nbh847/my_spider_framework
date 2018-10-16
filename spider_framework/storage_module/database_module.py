from ..utils_module.log_module import get_logger
from .items import db, GoodsShop


class DBOperation:

    def __init__(self):
        self.logger = get_logger()

    def insert_data(self, data, table_name='', type='mysql'):
        if type == 'mysql':
            if table_name:
                self._insert_to_db(data, table_name)
            else:
                self.logger.warning('请输入数据库的表名, table name')
        elif type == 'es':
            pass
        else:
            self.logger.warning('输入的数据库类型type: {} 不对，请重新输入.'.format(type))

    def _insert_to_db(self, data, table_name, retry=3):
        # 插入数据到数据库
        db_table = locals()[table_name]
        try:
            # 查看建表信息，没有则新建表
            if not db_table.table_exists():
                db_table.create_table()

            # 执行数据库操作
            db_table.create(
                xxx='xxx',
                sss='sss',
            )

        except Exception as e:
            if str(e.args[0]) == '2013' or str(e.args[0]) == '2006' or str(e.args[0]) == '0':
                self.logger.info("重试次数还剩:{}次".format(retry))
                if retry < 1:
                    self.logger.warning('数据库重连次数到达{}次，退出。'.format(retry))
                    return

                self.logger.error('数据库已断开：{}'.format(e))
                self.logger.error('重连数据库')
                db.close()
                db.get_conn().ping(True)
                return self._insert_to_db(data, table_name, retry=retry-1)
            else:
                self.logger.warning('非数据库重连错误')
                raise e