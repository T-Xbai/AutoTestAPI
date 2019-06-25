# -- coding: utf-8 --
from app.utils.mongo_util import MongoUtil
from app.utils.mysql_util import MysqlUtil
import re


class DatabaseOper:

    def __init__(self, data_config: dict):
        self.database_type = data_config['database_type'].lower()
        host = data_config['host']
        username = data_config['username']
        password = data_config['password']
        database_name = data_config['database_name']

        if self.database_type == 'mysql':
            self.db = MysqlUtil(
                host=host,
                user=username,
                password=password,
                database=database_name
            )

        elif self.database_type == "mongo":
            try:
                ssh = data_config['ssh']
                self.db = MongoUtil(database=database_name, ssl=ssh)
            except KeyError:
                self.db = MongoUtil(database=database_name, host=host, username=username, password=password)

    def run_sql(self, sql: str):
        """
        根据已连接的数据库，执行对应的 sql
        :param database_type: 数据库类型
        :param sql: 执行的sql
        """
        if self.database_type == 'mysql':
            execute = getattr(self.db, "execute")
            return execute(sql)
        elif self.database_type == 'mongo':
            # 获取要操作的 集 、方法 、 过滤条件、修改值
            obj = self.mongo_match_sql(sql)
            collection_name = obj[0]
            method = obj[1]
            handle_sql = eval(obj[2])
            filter_sql = None
            set_sql = None
            if type(handle_sql) == tuple:
                filter_sql = handle_sql[0]
                set_sql = handle_sql[1]
            else:
                filter_sql = handle_sql

            # 需要操作的 集
            collection = getattr(self.db, 'collection')
            collection(collection_name)

            # 操作对应的 方法
            if hasattr(self.db, method):
                execute = getattr(self.db, method)
                if set_sql is not None:
                    return execute(filter_sql, set_sql)
                else:
                    return execute(filter_sql)
            else:
                raise Exception("找不到该执行方法：%s" % method)

    def mongo_match_sql(self, sql: str):
        """
        使用正则匹配 mongo 的 sql 语句
        :param sql: 固定格式： F_User:update_one({'user':'1111','passwd':'332211'},{'$set':{'phone':'136819111'}})
        集合：方法（{过滤条件},{修改值}）
        :return: 集 ， 方法，过滤条件，修改的值
        """

        regular = r"(.*):(.*)\(({.*})\)$"
        obj = re.match(r"(.*):(.*)\(({.*})|({.*}),({.*})\)$", sql, re.M | re.I)
        return obj.groups()

#
# if __name__ == '__main__':
#     database = DatabaseOper(
#         database_type='mongo',
#         database_name='ch_node',
#         ssl='mongodb://root:Hifox2017@dds-uf6cd3ffc59e27e41237-pub.mongodb.rds.aliyuncs.com:3717,dds-uf6cd3ffc59e27e42404-pub.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-3162811&authSource=admin'
#     )
#     sql = 'F_User:update_one({"phone":"136819507856"},{"$set":{"phone":"13681950785"}})'
#     database.run_sql(sql)
