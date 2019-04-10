# -- coding: utf-8 --
from utils.read_json_util import read_json
from utils.request_method_util import RequestMethodUtil


class RequestOper:
    url = ''
    method = ''
    headers = {}
    rely_case = {}
    body = None
    response_assert = {}
    after = {}

    def __init__(self, file_name):
        case_data = read_json(file_name=file_name)

        self.url = case_data['url']
        self.method = case_data['method']
        self.headers = case_data['headers']
        self.rely_case = case_data['rely_case']
        self.body = case_data['body']
        self.response_assert = case_data['assert']
        self.after = case_data['after']

    def case_run(self):
        """
        case 运行方法
        :return: 运行结果
        """
        re = RequestMethodUtil()
        result = re.run(
            method=self.method,
            url=self.url,
            headers=self.headers,
            body=self.body,
        )
        return result


