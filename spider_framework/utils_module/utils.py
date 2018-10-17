from .log_module import get_logger, save_file_logger
from .date import Date
from ..config import *
from date_module import Date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

import requests
import json
import socket
import smtplib
import os
import time
import random
import datetime


class Utility:
    """
    这是一个工具库，集成平时会复用的方法
    """

    def __init__(self):
        self.logger = get_logger()

    def get_cookies_from_pool(self, website, username):
        '''
        这个方法是用来从cookie池获取cookies绕过登录
        '''
        self.logger.info('获取cookies')
        req = requests.get('http://10.0.5.58:7901/cookies?website={}&username={}'.format(website, username)).text
        # req = requests.get('http://localhost:4500/cookies?website={}&username={}'.format(website, username)).text
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

    def deploy_logs(self, project_name, whole_time, error_details, status_code, log_name='', **kwargs):

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
        self.logger.info("本机名称：{}".format(machine))
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
        if log_name:
            self.logger.info('有log name: {}'.format(log_name))
            save_logger = save_file_logger(file_path + '/{}.stdout.{}.log'.format(log_name, today))
        else:
            save_logger = save_file_logger(file_path + '/crawlers.stdout.{}.log'.format(today))
        self.logger.info("开始写入日志")
        save_logger.info(insert_data)
        self.logger.info("写入日志完成")

    def get_host_ip(self):
        '''
        获取本机IP
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

    def is_alive(self, ip):
        '''
        判断ip是否有效
        '''
        test_url = 'http://www.baidu.com/'
        proxy = {'http': "http://" + ip, 'https': "http://" + ip}
        try:
            req = requests.get(test_url, timeout=30, proxies=proxy)
            if req.status_code == 200:
                self.logger.info("status code: {}, ip: {} 可用".format(req.status_code, ip))
                return True
            else:
                self.logger.info("status code: {}, ip: {} 不可用".format(req.status_code, ip))
                return False
        except Exception as e:
            self.logger.info('bad ip %s' % ip)
            self.logger.warning('错误详情：{}'.format(e))
            return False

    def xstr(self, s):
        '''
        用来把 s 转为字符串，如果 s 为0， 则返回 ''
        '''
        if s is None:
            return ''
        return str(s)

    def get_ip_from_pool(self):
        '''
        从IP池获取IP，没有IP则返回空str
        :return:
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

    def send_email(self, warning_project):
        '''
        发送邮件模块, 可以带附件
        '''

        now = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        if warning_project:

            self.logger.info("需要报警的项目：{}".format(warning_project))

            # 发送邮件
            my_sender = '***@qq.com'
            my_pass = '****'
            my_user_list = ['****@qq.com']

            try:
                # 创建带附件的实例
                for user in my_user_list:
                    message = MIMEMultipart()
                    message['From'] = Header(my_sender, 'utf-8')
                    message['To'] = Header(user, 'utf-8')
                    subject = '{}的爬虫报警内容'.format(now)
                    message['Subject'] = Header(subject, 'utf-8')

                    # 邮件正文内容
                    message.attach(MIMEText('{}在{}没有任何数据，请检查对应的项目。'.format(warning_project, now), 'plain', 'utf-8'))

                    # 构造附件1，path路径下的文件
                    # att1 = MIMEText(open(path, 'rb').read(), 'plain', 'utf-8')
                    # att1["Content-Type"] = 'application/octet-stream'
                    # # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
                    # att1["Content-Disposition"] = 'attachment; filename="redbook_title{}.xlsx"'.format(now)
                    # message.attach(att1)

                    # # 构造附件2，传送当前目录下的 runoob.txt 文件
                    # att2 = MIMEText(open('runoob.txt', 'rb').read(), 'base64', 'utf-8')
                    # att2["Content-Type"] = 'application/octet-stream'
                    # att2["Content-Disposition"] = 'attachment; filename="runoob.txt"'
                    # message.attach(att2)

                    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
                    server.login(my_sender, my_pass)
                    server.sendmail(my_sender, [user, ], message.as_string())
                    self.logger.info("邮件发送成功")
                    server.quit()
                    time.sleep(random.randint(3, 6))
            except Exception as e:
                self.logger.exception("发送邮件错误详情：{}".format(e))

        else:
            self.logger.info("今天:{}没有需要报警的项目".format(now))

    def send_to_dingding(self, warning_project, warning_data, inform_url="****"):

        '''
        发送钉钉通知模块
        '''

        now = (datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y-%m-%d %H:%M:%S")
        if warning_project:
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": '{}有报警情况'.format(now),
                    "text": "**{0}**\n"
                            "\n**报警的项目：**{1}\n"
                            "\n**报警的时间：**{2}\n"
                            "\n**报警的原因以及处理：**{3}\n"
                            "\n**报警的环境：**{4}".format('报警提示:', warning_project, now, warning_data, self.get_mechine())
                }
            }
            try:
                r = requests.post(inform_url, headers=self.headers, timeout=30, data=json.dumps(data))
                self.logger.info(r.status_code)
            except Exception as e:
                self.logger.exception("发送到钉钉消息error:{}".format(e))
                self.logger.warning("发送钉钉报警内容失败")
        else:
            self.logger.info("今天:{}没有需要报警的项目".format(now))
