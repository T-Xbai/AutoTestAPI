# -- coding: utf-8 --
import os


def getCatalogFilePath(catalog=None):
    """
    获取目录下的所有文件的路径
    :param catalog: 目录位置
    :return: 文件地址的集合
    """
    file_paths = []

    if catalog is None:
        catalog = "../test_data"

    for root, dirs, files in os.walk(catalog):
        for file in files:
            file_paths.append(root + '\\' + file)
    return file_paths
