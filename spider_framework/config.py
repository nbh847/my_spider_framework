'''
配置文件
'''
USER_AGENT = ''
SAVE_LOG_DEBUG_LEVEL = 'debug'
MY_DEBUG_LEVEL = 'debug'

# MYSQL config
MYSQL_DB_NAME = 'checkin'
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_CHARSET = 'utf8mb4'

# -----------------Redis config-----------------
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB_ID = 0

# -----------------api 设置-----------------
# 获取内容失败
FAILED_CODE = 400
# 获取内容成功
SUCCESS_CODE = 200
# api debug模式默认开启
DEBUG_STATUS = True
# api 地址
API_HOST = 'localhost'
API_PORT = 4500

# 日志保存路径
FILE_PATH = '/Users/weasny/company/logs'

# es 地址
ES_ADDRESS = 'http://.......'
