#! python3
# API执行入口

from flask import Flask
from flask_restful import Resource, Api, reqparse
from .utils_module.api_handler import handler
from .config import *

# API入口
app = Flask(__name__)
api = Api(app)

# parser是参数设置
parser = reqparse.RequestParser()
parser.add_argument('ip', type=str, default="", help="可用IP")
parser.add_argument('confirm', type=str, default="", help="确认删除")


# 从IP池获取IP
class GetIpFromPool(Resource):
    def get(self):
        # 获取一个IP
        result = handler.get_all_ip()
        if result['result'] is 1:
            return result, FAILED_CODE
        return result, SUCCESS_CODE

    def post(self):
        # 删除IP
        pass


api.add_resource(GetIpFromPool, '/ip')

if __name__ == "__main__":
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG_STATUS)
