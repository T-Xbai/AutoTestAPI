# -- coding: utf-8 --
from pymongo import MongoClient


class MongoUtil:
    """
    Mongo 的操作基类
    """

    def __init__(self, host: str, username, password, database, ssl=None):
        if host is None or host.lower() == 'null' \
                or host == '':
            self.client = MongoClient(ssl)
        else:
            self.client = MongoClient(host=host, username=username, password=password)

        try:
            self.db = self.client[database]
        except KeyError:
            raise KeyError("Mongo - 没有这个数据库：%s" % database)

    def collection(self, collection_name):
        try:
            self._collection = self.db[collection_name]
        except KeyError:
            raise KeyError("Mongo - 没有这个集合：%s" % collection_name)

    def find(self, filter):
        return self._collection.find(filter)

    def insert_one(self, insert_data: dict):
        self._collection.insert_one(insert_data)

    def insert_many(self, insert_datas: list):
        self._collection.insert_many(insert_datas)

    def update_one(self, filter, update):
        self._collection.update_one(filter, update)

    def update_many(self, filter, update):
        self._collection.update_many(filter, update)

    def del_one(self, filter):
        self._collection.delete_one(filter)

    def del_many(self, filter):
        self._collection.delete_many(filter)

    def __del__(self):
        self.client.close()
