from ..utils_module.log_module import get_logger
from .items import db, GoodsShop
from elasticsearch import Elasticsearch
from ..config import *


class DBOperation:

    def __init__(self):
        self.logger = get_logger()
        self.es = Elasticsearch(ES_ADDRESS)

    def operate_data(self, data, operation='', table_name='', index='', type='mysql'):
        if type == 'mysql':
            if table_name:
                if operation == 'insert':
                    self._insert_to_db(data, table_name)
                elif operation == 'get':
                    self._get_data_from_db(data, table_name)
                elif operation == 'delete':
                    self._delete_data_from_db(data, table_name)
                elif operation == 'update':
                    self._update_data_from_db(data, table_name)
                else:
                    self.logger.warning('请输入正确的operation')
            else:
                self.logger.warning('请输入数据库的表名, table name')
        elif type == 'es':
            if index:
                if operation == 'update':
                    self._update_data_from_es(data, index)
                elif operation == 'get':
                    self._get_data_from_es(data, index)
                elif operation == 'delete':
                    self._delete_data_from_es(data, index)
                else:
                    self.logger.warning('请输入正确的operation')
            else:
                self.logger.warning('请输入es的index')
        else:
            self.logger.warning('输入的数据库类型type: {} 不对，请重新输入.'.format(type))

    def _insert_to_db(self, data, table_name, retry=3):
        '''
        插入数据到数据库
        :param data: 被写入的数据
        :param table_name: 数据库表名
        :param retry: 重试次数
        :return: None
        '''
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
                return self._insert_to_db(data, table_name, retry=retry - 1)
            else:
                self.logger.warning('非数据库重连错误')
                raise e

    def _get_data_from_db(self, data, table_name, retry=3):
        '''
        从数据库获取数据
        :param data: 被写入的数据
        :param table_name: 数据库表名
        :param retry: 重试次数
        :return: None
        '''
        db_table = locals()[table_name]
        try:
            # 查看建表信息，没有则新建表
            if not db_table.table_exists():
                db_table.create_table()

            # 执行数据库操作
            xxx = db_table.select().limit(1 * 2)
            return xxx

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
                return self._insert_to_db(data, table_name, retry=retry - 1)
            else:
                self.logger.warning('非数据库重连错误')
                raise e

    def _delete_data_from_db(self, data, table_name, retry=3):
        '''
        从数据库删除数据
        :param data: 要被删除的数据
        :param table_name: 数据库表名
        :param retry: 重试次数
        :return: None
        '''
        db_table = locals()[table_name]
        try:
            # 查看建表信息，没有则新建表
            if not db_table.table_exists():
                db_table.create_table()

            # 执行数据库操作
            db_table.delete().where(db_table.xxx == 'xxx').execute()

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
                return self._insert_to_db(data, table_name, retry=retry - 1)
            else:
                self.logger.warning('非数据库重连错误')
                raise e

    def _update_data_from_db(self, data, table_name, retry=3):
        '''
        从数据库 更新 数据
        :param data: 要被 更新 的数据
        :param table_name: 数据库表名
        :param retry: 重试次数
        :return: None
        '''
        db_table = locals()[table_name]
        try:
            # 查看建表信息，没有则新建表
            if not db_table.table_exists():
                db_table.create_table()

            # 执行数据库操作
            db_table.update(off_shelf_status=True).where(db_table.xxx == 'xxx').execute()

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
                return self._insert_to_db(data, table_name, retry=retry - 1)
            else:
                self.logger.warning('非数据库重连错误')
                raise e

    def _get_data_from_es(self, data, index, doc_type='data'):
        '''
        es 查询操作
        :param index: 目标数据的索引
        :param body: es 查询语句
        :param doc_type: 类型，默认 data
        :return: 返回 dict 数据
        '''
        body = data  # ...
        return self.es.search(index, doc_type, body=body)

    def _update_data_from_es(self, data, index, doc_type='data'):
        '''
        es 查询操作
        :param index: 目标数据的索引
        :param body: es 查询语句
        :param doc_type: 类型，默认 data
        :return: 返回 dict 数据
        '''
        body = list()
        for j in data:
            if j:
                my_id = j['id']
                data = j['data']
                body.append({'update': {'_id': my_id, '_type': doc_type, '_index': index}})
                body.append({'doc': data, 'doc_as_upsert': True})
        if body:
            self.es.bulk(body)

    def _delete_data_from_es(self, data, index, doc_type='data'):
        '''
        es 查询操作
        :param index: 目标数据的索引
        :param body: es 查询语句
        :param doc_type: 类型，默认 data
        :return: 返回 dict 数据
        '''
        self.es.delete(index=index, doc_type=doc_type, id=data['id'])