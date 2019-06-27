# -- coding: utf-8 --
import json

import pytest
from jsonpath import jsonpath
from requests import Response

from app.utils.excel_util import ExcelUtil
from app.oper.excel_run_oper import ExcelRunOper
import app.test.globals as glo

glo.case_datas = ExcelUtil().getExcelData()


@pytest.mark.parametrize('case', glo.case_datas)
def test_func(case):
    excelRun = ExcelRunOper(case)
    if excelRun.is_run.upper() == 'Y':
        excelRun.dependRun()
        result = excelRun.runCase()

        asserts = excelRun.request_data.asserts
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
    pytest.main([
        '--alluredir=../report/allure_results'

    ])
