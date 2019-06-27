# -- coding: utf-8 --
from requests import Response

from app.oper.database_oper import DatabaseOper
from app.teamplate.excel_template import *
from app.utils.http_request_util import HttpRequestUtils as httpRequest
from app.utils.mysql_util import MysqlUtil
from app.utils.read_json_util import ReadJsonUtils
from app.utils.excel_util import ExcelUtil
from app.exception.execption import FormatError, ExperError
from app.utils.common_util import getYaml
from jsonpath import jsonpath
import json


class ExcelRunOper:

    def __init__(self, row_data: dict):
        """
        :type row_data: dict
        """
        self.case_number = row_data[CASE_NUMBER]
        self.test_goal = row_data[TEST_GOAL]
        self.test_port = row_data[TEST_PORT]
        self.request_method = row_data[REQUEST_METHOD]
        self.request_data = ReadJsonUtils(row_data[REQUEST_DATA])
        self.is_run = row_data[IS_RUN]
        self.is_pass = row_data[IS_PASS]

    def runCase(self):

        """
        case 运行，files 不为 null 会优先传入 files 的值
        :return:
        """

        body = self.request_data.body
        files = self.request_data.files

        result = None
        if files is not None:
            result = httpRequest.run(
                method=self.request_data.method,
                url=self.request_data.url,
                files=files,
                headers=self.request_data.haders
            )
        else:
            if type(body) == dict:
                result = httpRequest.run(
                    method=self.request_data.method,
                    url=self.request_data.url,
                    json=body,
                    headers=self.request_data.haders
                )
            else:
                result = httpRequest.run(
                    method=self.request_data.method,
                    url=self.request_data.url,
                    data=body,
                    headers=self.request_data.haders
                )
        return result

    def dependRun(self):
        rely_cases = self.request_data.rely_cases
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
                if not excelRun.request_data.rely_cases is None: excelRun.dependRun()
                response = excelRun.runCase()

                if fields is None:
                    continue

                # 从响应文本中获取值，并替换请求数据
                variableValues = self.getDependFieldValues(response.text, fields)
                for variable, value in variableValues.items():
                    self.request_data.replaceVariable(variable, value)

    def getDependFieldValues(self, resBody, fields: dict):
        """
        获取依赖字段的值
        :param resBody: 响应信息
        :param fields: 依赖字段
        """
        resBody = json.loads(resBody)
        variable = {}
        for key, expr in fields.items():
            if expr[0:2] == '$.':
                value = jsonpath(resBody, expr)
                if value == False:
                    message = "表达式错误：[%s]  匹配结果为：False" % expr
                    raise ExperError(message)

                if type(value) == list:
                    value = value[0]
                variable[key] = value
            else:
                # TODO 正则表达式匹配数据，待完善
                pass

        return variable

    def assertExpectedResult(self, result: Response):
        """
        统一断言方法
        """
        asserts = self.request_data.asserts
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

    def dbExecute(self, database: str):
        """
        根据配置，连接数据库
        :param database: 数据库名称
        :return: MysqlUtil
        """
        db_config = self.request_data.db_config
        if db_config is None:
            db_config = getYaml('db')

        return DatabaseOper(db_config, database)

    def after_run(self, result: Response):
        """
        后置处理运行，主要针对数据库修改数据
        """
        afters_conf = self.request_data.after

        variables = self._key_is_exist('variables', afters_conf)
        if variables is not None:
            dependFielValues = self.getDependFieldValues(result.text, variables)
            for key, value in dependFielValues.items():
                self.request_data.replaceVariable(key, value)
            afters_conf = self.request_data.after

        executes = self._key_is_exist("executes", body=afters_conf)

        if executes is not None:
            for execute in executes:
                db = self.dbExecute(self._key_is_exist("name", execute))
                sqls = self._key_is_exist('sql', execute)
                if sqls is not None:
                    for sql in sqls:
                        query_res = db.run_sql(sql)
                        print("query result : %s \n" % query_res)

    def _key_is_exist(self, key, body):
        return self.request_data.key_is_exist(key, body=body)


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
    excelRun.after_run(result)
