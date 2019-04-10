# -- coding: utf-8 --
from json import JSONDecodeError

from requests import Response


class ResponseOper:

    def __init__(self, response: Response):
        response.encoding = 'utf-8'
        self.code = response.status_code
        try:
            self.body = response.json()
        except JSONDecodeError:
            self.body = response.text
        self.request_url = response.url

    def get_rely_fields_value(self, fields: list):
        if fields == 'null' or len(fields) < 1:
            raise Exception("依赖字段的不得为空: %r" % fields)
        bodys = {}
        for field in fields:
            try:
                bodys[field] = self.body[field]
            except KeyError:
                raise Exception("响应文本内找不到该依赖字段： %r" % field)
        return bodys


# if __name__ == '__main__':
#     from oper.request_oper import RequestOper
#
#     re = RequestOper("test_login.json")
#     result = re.case_run()
#     response = ResponseOper(result)
    # print(response.code)
    # print(type(response.body))
    # print(type(response.json))
    # print(response.json)
    # print(response.body)
    # rely_field_values = response.get_rely_fields_value([])
    # print(rely_field_values)
