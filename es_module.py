'''
es 操作模块
'''

from elasticsearch import Elasticsearch
from setting_module import ES_ADDRESS


class ESModule:
    '''
    elasticsearch 操作类
    '''

    def __init__(self):
        self.es = Elasticsearch(ES_ADDRESS)

    def update(self, index, my_id, json_data, doc_type='data'):
        '''
        es 更新操作
        :param index: es 的索引
        :param my_id: 每条数据的 ID
        :param json_data: 需要写入的 json 数据
        :param doc_type: 类型，默认为 data
        :return: None
        '''
        body = list()
        body.append({'update': {'_id': my_id, '_type': doc_type, '_index': index}})
        body.append({'doc': json_data, 'doc_as_upsert': True})
        self.es.bulk(body)

    def delete(self, index, my_id, doc_type='data'):
        '''
        es 删除操作
        :param index: es 的索引
        :param my_id: 每条数据的 ID
        :param doc_type: 类型，默认为 data
        :return: None
        '''
        self.es.delete(index=index, doc_type=doc_type, id=my_id)
