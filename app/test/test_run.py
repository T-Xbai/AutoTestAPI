# -- coding: utf-8 --
import json
from json import JSONDecodeError
import pytest
from jsonpath import jsonpath
from app.utils.excel_util import ExcelUtil
from app.oper.excel_run_oper import ExcelRunOper
from app.utils.common_util import Log
from app.teamplate.excel_template import *

case_datas = ExcelUtil().getExcelData()
log = Log().log


@pytest.mark.parametrize('case', case_datas)
def test_func(case):
    excelRun = ExcelRunOper(case)

    log.info(
        ">>>>>>>>>>>>>>>>>>>>>>>>>>>  run case : %s  <<<<<<<<<<<<<<<<<<<<<<<<<<" %
        case[CASE_NUMBER])
    if excelRun.is_run.upper() == 'Y':
        excelRun.depend_run()
        result = excelRun.run_case()

        asserts = excelRun.request_data.asserts
        if asserts is not None:
            for key, value in asserts.items():
                if key == 'code':
                    assert result.status_code == value
                elif key == 'isContains':
                    assert value in result.text
                else:
                    res_body = result.text
                    practical_res = None
                    try:
                        json_body = json.loads(result.text, encoding='utf-8')
                        practical_res = jsonpath(json_body, key)
                    except JSONDecodeError:
                        practical_res = res_body

                    if type(practical_res) == list:
                        practical_res = practical_res[0]
                    assert practical_res == value


if __name__ == '__main__':
    pytest.main([
        '--alluredir=../report/allure_results'
    ])
