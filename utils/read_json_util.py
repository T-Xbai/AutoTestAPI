# -- coding: utf-8 --
import json


def read_json(file_name):
    """
    读取 json 文件
    :param file_name: 文件名称 ，支持： login/login.json
    """
    json_file = '../test_data/json_data/' + file_name + '.json'
    with open(json_file, 'r') as f:
        return json.loads(f.read())






