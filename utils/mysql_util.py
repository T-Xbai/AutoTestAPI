# -- coding: utf-8 --

import pymysql
from pymysql import OperationalError


class MysqlUtil:
    """
    Mysql 的操作基类
    """

    def __init__(self, host, user, password, database):
        try:
            self.db = pymysql.connect(host=host, user=user, password=password, database=database)
            self.cursor = self.db.cursor()
        except OperationalError :
            raise OperationalError("无法连接 MySQL 服务")

    def execute(self, sql):
        """
        执行 SQL
        :param sql:  sql 语句
        :return: 返回数据返回加过
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def __del__(self):
        self.db.commit()
        self.db.close()