from setting_module import *
from log_module import get_logger

import redis

'''
redis 操作区域
'''


class RedisHash:
    '''
    redis hash 操作类
    '''

    def __init__(self, type, name):
        '''
        redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量;
        key 是hash的名称;
        type 是类型，比如：cookie， ip;
        name 是需要维护的网站名称，比如：sycm，huoniu；
        :param type:
        :param name:
        '''
        self.__db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_ID)
        self.key = '{type}:{user_name}'.format(type=type, user_name=name)
        self.logger = get_logger()

    def count(self):
        '''
        返回key对应的值的数量
        :return:
        '''
        return self.__db.hlen(self.key)

    def set(self, username, value):
        '''
        设置键值对
        :param username: 用户名
        :param value: 密码或者cookie
        :return:
        '''
        return self.__db.hset(self.key, username, value)

    def get(self, username):
        '''
        根据键名获取键值
        :param username: 用户名
        :return:
        '''
        return self.__db.hget(self.key, username)

    def delete(self, username):
        '''
        根据键名删除键值对
        :param username: 用户名
        :return:
        '''
        return self.__db.hdel(self.key, username)

    def all(self):
        '''
        获取所有键值对
        :return: 用户名和密码或Cookies的映射表
        '''
        return self.__db.hgetall(self.key)


class RedisQueue:
    '''
    redis queue 操作类
    '''

    def __init__(self, name, namespace='Base'):
        # redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量
        self.__db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_ID)
        self.key = '%s:%s' % (namespace, name)
        self.logger = get_logger()

    def qsize(self):
        return self.__db.llen(self.key)  # 返回队列里面list内元素的数量

    def put(self, item):
        if not self.is_item_exists(item):
            self.__db.rpush(self.key, item)  # 添加新元素到队列最右方
            self.logger.info("{}已加入队列".format(item))

    def put_to_top(self, item):
        if not self.is_item_exists(item):
            self.__db.lpush(self.key, item)  # 添加新元素到队列最左方
            self.logger.info("{}已加入队列".format(item))

    def get_wait(self, timeout=None):
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，超时则抛出异常，如果为None则一直等待）
        item = self.__db.blpop(self.key, timeout=timeout)
        if item:
            item = item[1].decode("utf-8")  # 返回值为一个tuple
        return item

    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.__db.lpop(self.key)
        if item:
            item = item.decode('utf8')  # 返回值为value
        return item

    def is_item_exists(self, item):
        # 判断item是否存在队列中
        return_status = False
        all_itmes = self.__db.lrange(self.key, 0, self.qsize())
        for ai in all_itmes:
            if ai.decode('utf8').split(';')[0] in item:
                self.logger.info("{}在队列中，重复了。".format(item))
                return_status = True
                return return_status
        return return_status
