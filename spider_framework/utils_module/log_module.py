import logging
from ..config import MY_DEBUG_LEVEL, SAVE_LOG_DEBUG_LEVEL
from logging import getLogger

'''
日志 模块
'''


def get_logger():
    '''
    打印到终端的日志
    '''
    logger = getLogger(__name__)
    if logger.handlers:
        for i in range(len(logger.handlers)):
            logger.handlers.pop()
    logger.setLevel('DEBUG')
    BASIC_FORMAT = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
    DATE_FORMAT = '%a, %Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
    chlr = logging.StreamHandler()  # 输出到控制台的handler
    chlr.setFormatter(formatter)
    chlr.setLevel(MY_DEBUG_LEVEL.upper())  # 也可以不设置，不设置就默认用logger的level
    logger.addHandler(chlr)
    return logger


def save_file_logger(file_path):
    '''
    保存到指定目录的日志
    '''
    file_logger = getLogger('save' + __name__)
    if file_logger.handlers:
        for i in range(len(file_logger.handlers)):
            file_logger.handlers.pop()
    file_logger.setLevel(SAVE_LOG_DEBUG_LEVEL.upper())
    fhlr = logging.FileHandler(file_path)  # 输出到文件的handler
    file_logger.addHandler(fhlr)
    return file_logger
