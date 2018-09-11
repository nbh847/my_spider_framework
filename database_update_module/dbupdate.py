'''
数据库跟踪模块
'''

from .pw_migrage_module import run
import os

current_path = os.path.dirname(__file__)

run(current_path + '/migrations')
