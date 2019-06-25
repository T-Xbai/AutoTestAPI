# -- coding: utf-8 --
from requests import Response

from app.teamplate.excel_template import *
from app.utils.http_request_util import HttpRequestUtils as httpRequest
from app.utils.read_json_util import ReadJsonUtils
from app.utils.excel_util import ExcelUtil
from app.exception.execption import FormatError, ExperError
from jsonpath import jsonpath
import json


class ExcelRunOper:

    def __init__(self, row_data: dict):

        self.CASE_NUMBER = row_data[CASE_NUMBER]
        self.TEST_GOAL = row_data[TEST_GOAL]
        self.TEST_PORT = row_data[TEST_PORT]
        self.REQUEST_METHOD = row_data[REQUEST_METHOD]
        self.REQUEST_DATA = ReadJsonUtils(row_data[REQUEST_DATA])
        self.IS_RUN = row_data[IS_RUN]
        self.IS_PASS = row_data[IS_PASS]

    def runCase(self):
        '''
        case 运行，files 不为 null 会优先传入 files 的值
        :return:
        '''
        body = self.REQUEST_DATA.body
        files = self.REQUEST_DATA.files

        result = None
        if files is not None:
            result = httpRequest.run(
                method=self.REQUEST_DATA.method,
                url=self.REQUEST_DATA.url,
                files=files,
                headers=self.REQUEST_DATA.haders
            )
        else:
            if type(body) == dict:
                result = httpRequest.run(
                    method=self.REQUEST_DATA.method,
                    url=self.REQUEST_DATA.url,
                    json=body,
                    headers=self.REQUEST_DATA.haders
                )
            else:
                result = httpRequest.run(
                    method=self.REQUEST_DATA.method,
                    url=self.REQUEST_DATA.url,
                    data=body,
                    headers=self.REQUEST_DATA.haders
                )
        return result

    def dependRun(self):
        rely_cases = self.REQUEST_DATA.rely_cases
        if not rely_cases is None:
            for rely_case in rely_cases:
                case_id = rely_case['case_id']
                fields = rely_case['fields']
                row = None

                try:
                    sheetName, caseNumber = case_id.split('.')
                    row = ExcelUtil().sheetOnRowValues(sheetName, caseNumber)

                except ValueError:
                    raise FormatError("key ：case_id 的值格式不正确 %r" % case_id)

                excelRun = ExcelRunOper(row)
                # 判断依赖的case ，是否还有依赖的case ： 递归
                if not excelRun.REQUEST_DATA.rely_cases is None: excelRun.dependRun()
                response = excelRun.runCase()

                if fields is None:
                    continue

                # 从响应文本中获取值，并替换请求数据
                variableValues = self.getDependFieldValues(response.text, fields)
                for variable, value in variableValues.items():
                    self.REQUEST_DATA.replaceVariable(variable, value)

    def getDependFieldValues(self, resBody, fields: dict):
        '''
        获取依赖字段的值
        :param resBody: 响应信息
        :param fields: 依赖字段
        '''
        resBody = json.loads(resBody)
        variable = {}
        for key, expr in fields.items():
            value = jsonpath(resBody, expr)
            if value == False:
                message = "表达式错误：[%s]  匹配结果为：False" % expr
                raise ExperError(message)

            if type(value) == list:
                value = value[0]
            variable[key] = value

        return variable

    def assertExpectedResult(self, result: Response):
        asserts = self.REQUEST_DATA.asserts
        if asserts is not None:
            for key, value in asserts.items():
                if key == 'code':
                    assert result.status_code == value
                elif key == 'isContains':
                    assert value in result.text
                else:
                    res_json = json.loads(result.text, encoding='utf-8')
                    json_values = jsonpath(res_json, key)
                    if type(json_values) == list:
                        json_values = json_values[0]
                    assert json_values == value


if __name__ == '__main__':
    row_data = {
        "用例编号": "login_01",
        "测试目的": "登录",
        "测试接口": "/member/butler_login.do",
        "请求方法": "POST",
        "请求数据": "login/test_login_01",
        "是否执行": "Y",
        "是否通过": None
    }
    excelRun = ExcelRunOper(row_data)
    excelRun.dependRun()
    result = excelRun.runCase()
    excelRun.assertExpectedResult(result)
