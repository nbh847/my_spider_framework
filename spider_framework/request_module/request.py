from ..config import USER_AGENT
from ..utils_module.log_module import get_logger

import requests


class RequestModule:
    '''
    请求模块
    '''

    def __init__(self):
        self.logger = get_logger()

    def get_response(self, url, method='get', timeout=0, data_type='string', **kwargs):
        '''
        :param url: 请求的链接
        :param method: 请求的方式，默认是get方法
        :param timeout: 超时时间
        :param data_type: 请求的方式，默认是get方法
        :param kwargs: 请求内的方法，header，timeout 等选项
        :return: 返回请求到的响应
        '''
        headers = {
            'User-Agent': USER_AGENT,
        }
        for k, v in kwargs.items():
            # k 为 headers 表示传入了 headers 参数
            if k == 'headers':
                headers = v

        if method == 'get':
            return self._request_get(url, headers, timeout, data_type)
        elif method == 'post':
            return self._request_post(url, headers, timeout, data_type)
        else:
            self.logger.warning('参数 method 错误，请重试.')

    def _request_get(self, url, headers, timeout, data_type):
        if timeout:
            # 设置超时
            req = requests.get(url, headers=headers, timeout=timeout)
        else:
            req = requests.get(url, headers=headers)
        if data_type == 'byte':
            # 返回二进制
            return req.content
        return req.text

    def _request_post(self, url, headers, timeout, data_type):
        if timeout:
            # 设置超时
            req = requests.post(url, headers=headers, timeout=timeout)
        else:
            req = requests.post(url, headers=headers)
        if data_type == 'byte':
            # 返回二进制
            return req.content
        return req.text


if __name__ == '__main__':
    url = 'http://www.baidu.com/'
    r = RequestModule()
    req = r.get_response(url)
    # req = requests.get(url).text
    print(req)
