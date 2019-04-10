# -- coding: utf-8 --
import os


def getCatalogFilePath( catalog=None):
    file_paths = []

    if catalog is None:
        catalog = "../test_data"

    for root, dirs, files in os.walk(catalog):
        for file in files:
            file_paths.append(root + '\\' + file)
    return file_paths




if __name__ == '__main__':
    paths = getCatalogFilePath()
    print(paths)
