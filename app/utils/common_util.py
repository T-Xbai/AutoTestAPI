# -- coding: utf-8 --

import os, yaml, logging as log
from datetime import datetime

class Log:

    def __init__(self):
        filename = datetime.utcnow()
        log.basicConfig(
            filename='../report/%s.log' % filename,
            filemode='w',
            format='%(asctime)s %(name)s %(levelname)s :: %(funcName)s : %(message)s',
            level=log.DEBUG
        )

    @property
    def log(self):
        return log


def get_catalog_file_path(catalog=None):
    """
    获取目录下的所有文件的路径
    :param catalog: 目录位置
    :return: 文件地址的集合
    """
    file_paths = []

    if catalog is None:
        catalog = "../test_data/case_data"

    for root, dirs, files in os.walk(catalog):
        for file in files:
            file_format = file.split('.')[1]
            if file_format == 'xlsx':
                file_paths.append(root + '\\' + file)
    return file_paths


def get_yaml(key: str, file_path: str = None):
    if file_path is None:
        file_path = "../conf/conf.yaml"

    with open(file_path, 'rb') as f:
        values = yaml.load(f, Loader=yaml.FullLoader)
        return values.get(key)
