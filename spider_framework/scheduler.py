from spider_framework.request_module.request import RequestModule
from multiprocessing import Process
import redis

'''
爬虫调度器
'''


def temp_req():
    '''
    这是爬虫的逻辑区，用来根据url获取数据
    :return:
    '''
    while True:
        url = redis.get('url')
        if url:
            req = RequestModule()
            # run spider
            response = req.get_response(url)
        else:
            break


class Scheduler:
    '''
    爬虫调度器，开启多线程进行抓取，默认开启一个线程.
    '''
    def run(self, num=1):
        process_list = []
        for i in range(num):
            process_list.append(Process(target=temp_req))
        for p in process_list:
            p.start()
        for p in process_list:
            p.join()
