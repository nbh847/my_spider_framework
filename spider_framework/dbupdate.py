'''
数据库迁移脚本执行入口
'''
from .storage_module.pw_migrate import run
import os

current_path = os.path.dirname(__file__)

run(current_path+'/migrations')
