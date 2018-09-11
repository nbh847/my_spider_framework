'''
数据库模块
'''

# 主要是负责model模块
# -*- coding: utf-8 -*-

# Define here the models for your scraped items

import peewee as pw
from setting_module import *

db = pw.MySQLDatabase(MYSQL_DB_NAME, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                      charset=MYSQL_CHARSET)


# 代理ip
class Proxies(pw.Model):
    proxy_ip = pw.CharField(verbose_name="ip地址", primary_key=True, max_length=100)
    create_time = pw.DateTimeField(verbose_name="IP入库时间", default='1970-01-01')

    class Meta:
        database = db
