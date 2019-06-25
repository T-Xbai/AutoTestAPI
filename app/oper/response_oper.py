# -- coding: utf-8 --
from json import JSONDecodeError

from requests import Response


class ResponseOper:
    """
    响应结果处理类
    """

    def __init__(self, response: Response):
        response.encoding = 'utf-8'
        self.code = response.status_code
        try:
            self.body = response.json()
        except JSONDecodeError:
            self.body = response.text
        self.request_url = response.url
        print("Response code: %r" % self.code)
        print("Response body: %r" % self.body)

    def get_rely_fields_value(self, fields: list):
        """
        获取依赖字段的值
        :param fields: 依赖字段
        :return: 字段值
        """
        if fields == 'null' or fields is None or len(fields) < 1:
            return None
        bodys = {}
        for field in fields:
            try:
                bodys[field] = self.body[field]
            except KeyError:
                raise Exception("响应文本内找不到该依赖字段： %r" % field)
        return bodys
