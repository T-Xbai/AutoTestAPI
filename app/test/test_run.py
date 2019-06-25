# -- coding: utf-8 --
import pytest
from app.oper import DatabaseOper
from app.utils.excel_util import ExcelUtil
from app.utils import read_json

database_oper = None
excel = None
excel_cases = []


@pytest.fixture(scope='class', autouse=True)
def set_up_class():
    global database_oper, excel, excel_cases
    file_path = '../test_data/case_data/test_case.xlsx'
    excel = ExcelUtil(file_path)
    excel_cases = get_excel_cases(excel.getExcelData())

    config = excel.getConfig()
    database_oper = DatabaseOper(data_config=config)


def get_excel_cases(excel_data: dict):
    """
    将每个sheet 下面的case整合成一个list
    """

    cases = []
    for key, value in excel_data.items():
        cases += value
    return cases


@pytest.mark.usefixtures('set_up_class')
class TestRun:

    @pytest.mark.parametrize('case_datas', excel_cases)
    def test_run(self, case_datas):
        case_datas

    def run_case(self, case_datas: dict):
        json_file_name = case_datas['请求数据']
        request_data = read_json(json_file_name)
        try:
            rely_case = request_data['rely_case']
            if rely_case != 'null':



        except KeyError:


if __name__ == '__main__':
    pytest.main([
        '-s',
        'test_run.py'
    ])
