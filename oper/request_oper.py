# -- coding: utf-8 --
from oper.response_oper import ResponseOper
from utils.excel_util import ExcelUtil
from utils.read_json_util import read_json
from utils.request_method_util import RequestMethodUtil
from teamplate.excel_template import REQUEST_DATA, CASE_NUMBER, TEST_URL
from teamplate.json_teamplate import RELY_CASE, METHOD, URL, HEADERS, BODY


class RequestOper:
    """
    数据请求的操作类
    """

    def __init__(self, case_data, rely_fields=None):
        self.excel = ExcelUtil()
        self.request_data = read_json(case_data[REQUEST_DATA])
        self.request_data = self.replace_url_host()
        self.rely_fields = rely_fields

    def run_case(self):
        rely_datas = self.get_rely_case()
        if rely_datas is not None:
            if type(rely_datas) == list:
                for rely_data in rely_datas:
                    self.run_rely_data(rely_data)
            elif type(rely_datas) == dict:
                self.run_rely_data(rely_datas)

        response = self._run()
        return response.get_rely_fields_value(self.rely_fields)

    def run_rely_data(self, rely_datas):
        """
        处理并运行依赖数据后，替换请求数据中的变量
        """
        for rely_case, rely_fields in rely_datas.items():
            sheet_name, case_number = rely_case.split(">")
            rely_case_data = self.get_case_data(sheet_name, case_number)
            re_oper = RequestOper(rely_case_data, rely_fields)
            rely_field_values = re_oper.run_case()
            self.request_data = self.replace_request_data(self.request_data, rely_field_values)

    def get_case_data(self, sheet_name, case_number):
        """
        根据工作溥名称，与用例编号，获取对应的用例数据
        """
        excel_data = self.excel.getExcelData()
        sheet_data = excel_data[sheet_name]
        for case_data in sheet_data:
            if case_number == case_data[CASE_NUMBER]:
                return case_data

    def get_rely_case(self):
        """
        获取依赖数据
        """
        _rely_data = None
        try:
            _rely_data = self.request_data[RELY_CASE]
        except KeyError:
            _rely_data = None
        return _rely_data

    def _run(self):
        """
        case 运行方法
        :return: 运行结果
        """
        print("Request data : %s" % self.request_data)
        re = RequestMethodUtil()
        result = re.run(
            method=self.request_data[METHOD],
            url=self.request_data[URL],
            headers=self.request_data[HEADERS],
            body=self.request_data[BODY],
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
            value = str(value)
            replace_format = "{{ " + key + " }}"
            _request_data = _request_data.replace(replace_format, value)
        return eval(_request_data)

    def replace_url_host(self):
        """
        替换请求 URL 中设置的 {{ test_url }} 变量
        """
        config = self.excel.getConfig()
        return self.replace_request_data(self.request_data, {TEST_URL: config[TEST_URL]})


