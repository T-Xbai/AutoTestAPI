# -- coding: utf-8 --
from oper.response_oper import ResponseOper
from utils.read_json_util import read_json
from utils.request_method_util import RequestMethodUtil


class RequestOper:
    """
    数据请求的操作类
    """
    url = ''
    method = ''
    headers = {}
    rely_case = {}
    body = None
    response_assert = {}
    after = {}

    def __init__(self, file_name, rely_fields: dict = None):
        case_data = read_json(file_name=file_name)

        # 替换请求数据中使用的变量
        if rely_fields is not None:
            case_data = self.replace_request_data(case_data, rely_fields)

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
        return ResponseOper(result)

    def replace_request_data(self, request_data: dict, rely_fields: dict):
        """
        替换数据中使用的变量
        :param request_data: 请求数据
        :param rely_fields:  依赖字段
        :return: 替换后数据
        """
        _request_data = request_data
        if type(_request_data) == dict:
            _request_data = str(_request_data)
        for key, value in rely_fields.items():
            replace_format = "{{ " + key + " }}"
            _request_data.replace(replace_format, value)
        return eval(_request_data)
