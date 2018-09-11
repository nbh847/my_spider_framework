# 配置基本的数据库连接等信息

'''
配置文件模块
'''

# -----------------MYSQL config-----------------
MYSQL_DB_NAME = 'tools-keeper'  # tools-keeper
MYSQL_HOST = 'localhost'  # '10.0.0.40'
MYSQL_PORT = 3306
MYSQL_USER = 'root'  # 'outertest'
MYSQL_PASSWORD = 'yourdream'  # 'outertest'
MYSQL_CHARSET = 'utf8mb4'

# MYSQL_DB_NAME = 'tools-keeper'
# MYSQL_HOST = 'yourdream-crawler.mysql.rds.aliyuncs.com'
# MYSQL_PORT = 3306
# MYSQL_USER = 'crawler'
# MYSQL_PASSWORD = 'c,c(S#@*(*&@19jw'
# MYSQL_CHARSET = 'utf8mb4'

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
SYCM_COOKIES_PROCESS = False  # 生意参谋cookies进程开关
JD_COOKIES_PROCESS = True  # 京东cookies进程开关
XHS_COOKIES_PROCESS = False  # 小红书cookies进程开关
MASTER_COOKIES_PROCESS = False  # 达人商品下载cookies进程开关
HUPUN_COOKIES_PROCESS = False  # 万里牛ERP cookies进程开关

PURCHASED_IP_PROCESS = True  # ip池的进程开关

# -----------------request config-----------------
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko)' \
             ' Chrome/61.0.3163.100 Safari/537.36'
TMALL_REFERER = 'https://www.tmall.com/?spm=a220m.1000858.a2226n0.1.6305ea217Rf6db'
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
TOOLS_ADDRESS = '10.0.5.58:6821'

# file path 是日志文件的保存路径
FILE_PATH = '/Users/weasny/company/logs'

# phantomjs 的执行路径
PHANTOMJS_PATH = '/usr/local/bin/phantomjs'
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
FIREFOXDRIVER_PATH = '/usr/local/bin/geckodriver'

# -————————————————————暂停时间-————————————————————

# webdriver 的每次行动后的间隔时间
WEBDRIVER_DELAY_TIME = 2
