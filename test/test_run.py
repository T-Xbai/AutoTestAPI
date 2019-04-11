# -- coding: utf-8 --
import pytest
from utils.file_uitl import get_catalog_file_path
from utils.excel_util import ExcelUtil

files = get_catalog_file_path()


@pytest.fixture(scope='class', params=files, autouse=True)
def get_file_datas(request):
    file = request.param
    excel = ExcelUtil(file)
    excel_datas = excel.getExcelData()
    for case_data in excel_datas.items()[1]:



class TestRun:

    def test_run(self):
        print('----------------')


if __name__ == '__main__':
    pytest.main([
        '-v',
        'test_run.py'
    ])
