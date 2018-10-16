import os

'''
文件读写模块
'''


class FileOparetion:

    def __init__(self):
        pass

    @classmethod
    def read_file(cls, file_path, mode='r'):
        '''
        从文件里读数据
        :param file_path: 文件的绝对路径
        :param mode: 读写方式
        :return: 返回读取的数据
        '''
        cls.create_path(file_path)
        with open(file_path, mode=mode) as file:
            return file.read()

    @classmethod
    def save_file(cls, file_path, data, mode='w'):
        '''
        往文件里写数据
        :param file_path: 文件的绝对路径
        :param data: 要保存的数据
        :param mode: 读写方式
        :return: None
        '''
        cls.create_path(file_path)
        with open(file_path, mode=mode) as file:
            file.write(data)

    @classmethod
    def create_path(cls, file_path):
        '''
        如果 path 不存在，则创建 path
        :param file_path: 文件的绝对路径
        :return:
        '''
        if '/' in file_path:
            file_name = file_path.split('/')[-1]
            path = file_path.replace(file_name, '')
            if not os.path.exists(path):
                os.makedirs(path)
        else:
            return None


if __name__ == '__main__':
    path = '/Users/weasny/company/backstage_data/test_file/test.py'
    content = 'xixhaha'
    # FileOparetion.save_file(path, content)
    print(FileOparetion.read_file(path))
