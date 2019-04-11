# -- coding: utf-8 --
import pytest
from utils.file_uitl import get_catalog_file_path
from utils.excel_util import ExcelUtil

files = get_catalog_file_path()






@pytest.fixture(scope='function', autouse=True)
def setUpfunction():
    print('----------------------------------------------------------------------------------------------------')
