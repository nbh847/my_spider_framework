# 配置基本的数据库连接等信息

'''
配置文件模块
'''

# -----------------MYSQL config-----------------
MYSQL_DB_NAME = '*****'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '*****'
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

# API 开关
HUPUN_COOKIES_PROCESS = False

# ip池的进程开关
PURCHASED_IP_PROCESS = True

# -----------------request config-----------------
USER_AGENT = '*****'
# 重试次数
RETRY_TIMES = 6

'''
debug:logging.DEBUG, 
info:logging.INFO, 
error:logging.ERROR, 
'warning': logging.WARNING, 
'warn':logging.WARN
'''

# 本服务的IP地址
MY_DEBUG_LEVEL = 'info'
SAVE_LOG_DEBUG_LEVEL = 'INFO'
TOOLS_ADDRESS = '*****'

# file path 是日志文件的保存路径
FILE_PATH = '***'

# phantomjs 的执行路径
PHANTOMJS_PATH = '/usr/local/bin/phantomjs'
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
FIREFOXDRIVER_PATH = '/usr/local/bin/geckodriver'

# -————————————————————暂停时间-————————————————————

# webdriver 的每次行动后的间隔时间
WEBDRIVER_DELAY_TIME = 2

# es 地址
ES_ADDRESS = 'http://******'
