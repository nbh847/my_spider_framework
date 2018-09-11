import requests
from log_module import get_logger, save_file_logger
from setting_module import *
from date_module import Date

import json
import socket
import os

'''
工具库模块
'''


class Utility:
    """
    这是一个工具库，集成平时会复用的方法
    """

    def __init__(self):
        self.logger = get_logger()

    def delete_ip_from_pool(self, ip):
        '''
        从IP池删除IP
        '''
        req = requests.post('http://10.0.5.58:7901/ip?confirm=2&ip={}'.format(ip), timeout=30)
        if req.status_code == 200:
            self.logger.info('删除ip: {}成功'.format(ip))
        else:
            msg = json.loads(req.text)['msg']
            self.logger.info('删除ip: {}失败, 原因：{}'.format(ip, msg))

    def get_ip_from_pool(self):
        '''
        从IP池获取IP，没有IP则返回空str
        '''
        ip = requests.get('http://10.0.5.58:7901/ip', timeout=30)
        if ip.status_code == 200:
            proxy_ip = json.loads(ip.text)['data']['ip']
            self.logger.info("获取了IP: {}".format(proxy_ip))
            return proxy_ip
        else:
            msg = json.loads(ip.text)['msg']
            self.logger.info('获取ip失败, 原因：{}'.format(msg))
            return ''

    def get_cookies_from_pool(self, website, username):
        '''
        这个方法是用来从cookie池获取cookies绕过登录
        '''
        self.logger.info('获取cookies')
        req = requests.get('http://10.0.5.58:7901/cookies?website={}&username={}'.format(website, username)).text
        cookies = json.loads(req)['data']

        # 获取cookies
        mycookies = {}
        cookie_str = ''
        if cookies:
            try:
                self.logger.info("拿到了账户{}的cookies".format(username))
                for cookie in cookies:
                    mycookies[cookie['name']] = cookie['value']
                for c in mycookies:
                    cookie_str += "{}={};".format(c, mycookies[c])
                self.logger.info("cookie_str: {}".format(cookie_str))
            except Exception as e:
                self.logger.info('获取到了 str 类型的 cookies: {}'.format(e))
                return cookies
        else:
            self.logger.info("没有账户{}的cookies".format(username))
            cookie_str = ''
        return cookie_str

    def deploy_logs(self, project_name, whole_time, error_details, status_code, **kwargs):
        '''
        日志打点模块
        :param project_name: 项目名
        :param whole_time: 计时器的时间
        :param error_details: 错误详情
        :param status_code: 日志状态码，1：失败 or 0：成功
        :param kwargs: 附加参数
        :return: None
        '''
        # 防止不存在输出日志文件
        file_path = FILE_PATH
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        now = Date.now().format_es_utc_with_tz()
        host_ip = self.get_host_ip()
        if host_ip == '10.0.1.126':
            machine = 'apitest'
        elif host_ip == '10.0.5.58':
            machine = 'service1'
        elif host_ip == '10.0.5.59':
            machine = 'service2'
        elif host_ip == '192.168.8.117':
            machine = 'localhost'
        else:
            machine = 'other_mechine'
        # self.logger.info("本机名称：{}".format(machine))
        js_data = {
            'date': now,
            'machine': machine,
            'project_name': project_name,
            'whole_response_time': whole_time,
            'error_details': error_details,
            'status_code': status_code,  # int ,默认成功是0，其他的都是失败
        }
        for k, v in kwargs.items():
            js_data[k] = v

        js_data = json.dumps(js_data)
        insert_data = js_data

        # 写入到日志
        today = Date.now().format(full=False)
        save_logger = save_file_logger(file_path + '/crawlers.stdout.{}.log'.format(today))
        self.logger.info("开始写入日志")
        save_logger.info(insert_data)
        self.logger.info("写入日志完成")

    def get_host_ip(self):
        '''
        获取本机的 IP地址
        :return:
        '''
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception as e:
            self.logger.error("get host ip error:{}".format(e))
            ip = ''
        finally:
            s.close()
            return ip
