'''
数据库的module
'''

import peewee as pw
from ..config import *

db = pw.MySQLDatabase(MYSQL_DB_NAME, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                      charset=MYSQL_CHARSET)


# 天猫店铺的信息
class GoodsShop(pw.Model):
    shop_id = pw.CharField(primary_key=True, verbose_name="商店ID", max_length=30)
    shop_name = pw.CharField(verbose_name="店铺名称", max_length=100)
    create_time = pw.DateTimeField(verbose_name="创建时间", default='1970-01-01')

    class Meta:
        database = db
