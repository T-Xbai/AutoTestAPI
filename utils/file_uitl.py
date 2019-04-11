# -- coding: utf-8 --
import os


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
