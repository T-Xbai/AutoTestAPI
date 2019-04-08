# -- coding: utf-8 --
from utils.file_uitl import FileUtil
import os

if __name__ == '__main__':
    path = FileUtil().getCatalogFilePath()
    print(path)
