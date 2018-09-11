from log_module import get_logger
from setting_module import *

from flask import Flask
from flask_restful import Resource, Api, reqparse

'''
API 接口模块
'''

# ----------api 入库区 ------------
# API入口
app = Flask(__name__)
api = Api(app)

# parser是参数设置
parser = reqparse.RequestParser()
parser.add_argument('ip', type=str, default="", help="可用IP")


# 从IP池获取IP
class GetIpFromPool(Resource):
    def get(self):
        # 获取一个IP
        result = Handler().get_all_ip()
        if result['result'] is 1:
            return result, FAILED_CODE
        return result, SUCCESS_CODE

    def post(self):
        # 删除IP
        pass


api.add_resource(GetIpFromPool, '/ip')


# ----------api 逻辑处理区 ------------
class Handler(object):

    def __init__(self):
        self.logger = get_logger()

    def get_all_ip(self):
        '''
        获取IP池里所有的IP
        '''
        return_dic = {}
        return_dic['msg'] = "获取 全部IP 出错: {}。"
        return_dic['result'] = 1
        return_dic['data'] = ''
        return return_dic


# ----------API 启动入口-----------
if __name__ == "__main__":
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG_STATUS)
