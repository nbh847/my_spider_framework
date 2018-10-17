#! python3
from .log_module import get_logger

'''
API 逻辑处理区
'''


class Handler(object):

    def __init__(self):
        self.logger = get_logger()

    def get_all_ip(self):
        '''
        获取IP池里所有的IP
        '''
        return_dic = {}

        try:
            return_dic['msg'] = "返回获取的IP"
            return_dic['result'] = 0
            return_dic['data'] = 'sdf'
            return return_dic

        except Exception as e:
            self.logger.exception("获取 全部IP 出错: {}。".format(e))
            return_dic['msg'] = "获取 全部IP 出错: {}。".format(e)
            return_dic['result'] = 1
            return_dic['data'] = ''
            return return_dic


handler = Handler()
