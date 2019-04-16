# # -- coding: utf-8 --
import pytest

from oper.database_oper import DatabaseOper
from utils.common_util import get_catalog_file_path
from utils.excel_util import ExcelUtil

files = get_catalog_file_path()

excel_data = None
db = None


@pytest.fixture(scope='session', params=files, autouse=True)
def get_file_datas(request):
    file = request.param
    excel = ExcelUtil(file)
    config = excel.getConfig()
    if config['is_run'].lower() == 'y':
        db = get_config_data(config)
        excel_data = excel.getExcelData()
    else:
        excel_data = []





def get_config_data(config):
    """
    获取 config 数据库连接数据
    """
    database_type = config['database_type']
    database_name = config['database_name']
    host = config['host']
    username = config['username']
    password = config['password']
    ssh = config['ssh']

    return DatabaseOper(
        database_type=database_type,
        database_name=database_name,
        host=host,
        username=username,
        password=password,
        ssl=ssh
    )


class TestRun:

    def test_run(self):
        print('----------------')


if __name__ == '__main__':
    pytest.main([
        '-s',
        'test_run.py'
    ])
