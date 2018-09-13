'''
使用代理请求模块
'''

from log_module import get_logger
from utils_module import Utility
from setting_module import *
import requests
import random
import json


class ReqProxy:

    def __init__(self):
        self.logger = get_logger()

    def get_requests_by_proxy(self, sku_url):
        '''
        使用代理获取响应详情
        :param sku_url: 商品链接
        :return: sku api
        '''

        utils = Utility()
        account_list = ['***', '*****']
        ip = utils.get_ip_from_pool()
        if ip:
            self.logger.info("使用代理IP成功，ip: {}".format(ip))
            proxies = {
                "http": "http://{}".format(ip),
                "https": "http://{}".format(ip),
            }
            headers = {
                'User-Agent': USER_AGENT,
                'Referer': TMALL_REFERER,
            }
            try:
                sku_api = requests.get(sku_url, headers=headers, proxies=proxies, timeout=30).text
                self.logger.info("使用代理IP成功的sku api: {}".format(sku_api))
                test_sku_api = json.loads(sku_api.strip())
                if test_sku_api['isSuccess']:
                    self.logger.info('拿到商品的sku了')
            except Exception as e:
                self.logger.error("sku api error: {}".format(e))
                self.logger.info('没拿到商品的sku, 删除不可用IP: {}'.format(ip))
                utils.delete_ip(ip)
                sku_api = ''
            return sku_api
        else:
            user_agent = utils.get_random_user_agent()
            cookie_str = utils.get_cookies_from_pool('sycm', random.choice(account_list))
            headers = {
                'User-Agent': user_agent,
                'Referer': TMALL_REFERER,
                'Cookie': cookie_str,
            }
            try:
                sku_api = requests.get(sku_url, headers=headers, timeout=30).text
                self.logger.info("未获取到代理IP 的 sku api: {}".format(sku_api))
                test_sku_api = json.loads(sku_api.strip())
                if test_sku_api['isSuccess']:
                    self.logger.info('拿到商品的sku了')
            except Exception as e:
                self.logger.error("sku api error: {}".format(e))
                self.logger.info('没拿到商品的sku')
                sku_api = ''
            return sku_api
