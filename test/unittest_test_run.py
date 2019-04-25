# -- coding: utf-8 --
import unittest
from ddt import ddt, data, unpack

from oper.database_oper import DatabaseOper
from oper.request_oper import RequestOper
from utils.excel_util import ExcelUtil
from utils.read_json_util import read_json

excel = ExcelUtil()
db_oper = DatabaseOper(excel.getConfig())
excel_datas = excel.getExcelData()


def get_excel_cases(excel_datas: dict):
    datas = []
    for name, values in excel_datas.items():
        datas += values
    return datas


case_datas = get_excel_cases(excel_datas)


@ddt
class UnittestTestRun(unittest.TestCase):

    @data(*case_datas)
    def test_run(self, case_data):
        print('-------------------------------------------------------------------------------------------------------')
        print("Request case : %r" % case_data)
        is_run = case_data['是否执行']
        if is_run == "Y":
            re_oper = RequestOper(case_data)
            re_oper.run_case()

    # def run_rely_case(self, request_data: dict, fields=None):
    #     rely_datas = request_data["rely_case"]
    #     _rely_field_values = None
    #     if rely_datas != "null":
    #         if type(rely_datas) == list:
    #             for rely_data in rely_datas:
    #                 rely_request_data, rely_fields = self.get_rely_case_request_data(rely_data)
    #                 _rely_field_values = self.run_rely_case(rely_request_data, rely_fields)
    #         elif type(rely_datas) == dict:
    #             rely_request_data, rely_fields = self.get_rely_case_request_data(rely_datas)
    #             _rely_field_values = self.run_rely_case(rely_request_data, rely_fields)
    #         else:
    #             raise Exception("rely_case 字段的值类型错误 ：%s" % type(rely_datas))
    #
    #     request_oper = RequestOper(request_data,_rely_field_values)
    #     response = request_oper.case_run()
    #     rely_field_values = response.get_rely_fields_value(fields)
    #     return rely_field_values

    def get_rely_case_request_data(self, rely_data):
        """
        根据依赖case,获取对应的依赖请求数据
        :param rely_data:
        :return:
        """
        rely_case, rely_fields = rely_data.items()
        _case_data = None
        if ">" in rely_case:
            rely_sheet_name, rely_case_name = rely_case.split(">")
            sheet_datas = excel_datas[rely_sheet_name]
            for sheet_data in sheet_datas:
                case_name = sheet_data["用例编号"]
                if case_name == rely_case_name:
                    _case_data = sheet_data
        else:
            raise Exception('请求的json文件中，rely_case 字段名称命名不正确：%r' % rely_case)
        json_name = _case_data["请求数据"]
        return read_json(json_name), rely_fields


if __name__ == '__main__':
    unittest.main()
