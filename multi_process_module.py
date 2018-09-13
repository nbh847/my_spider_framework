'''
多线程模块
'''

from threading import Thread
from log_module import get_logger
from redis_module import RedisQueue
from utils_module import Utility


class ProxyCheck(Thread):

    def __init__(self):
        super(ProxyCheck, self).__init__()
        self.redis = RedisQueue('ip')
        self.my_utils = Utility()
        self.logger = get_logger()

    def run(self):
        '''
        事件执行入口
        '''
        while True:
            ip = self.redis.get_nowait()
            if ip:
                self.logger.info('测试IP：{}'.format(ip))
                self.ip_into_db(ip)
            else:
                self.logger.info("----------------------队列空了，测试完成。---------------------")
                break

    def ip_into_db(self, ip):
        '''
        执行方法
        '''
        pass


def start(threads=10):
    '''
    线程启动区，默认启动十个线程
    '''
    thread_list = list()
    for index in range(threads):
        thread_list.append(ProxyCheck())

    for thread in thread_list:
        thread.daemon = True
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == "__main__":
    start()
