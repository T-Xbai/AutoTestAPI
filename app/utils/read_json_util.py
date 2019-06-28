# -- coding: utf-8 --
import json
from app.utils.common_util import get_yaml


class ReadJsonUtils:
    json_values = None

    def __init__(self, file_path: str):
        self.json_values = self.read_json(file_path)

    def read_json(self, file_path: str) -> dict:

        '''
        读取 json 文件
        :param file_name: 文件名称 ，支持： login/login.json
        '''
        self.json_file = '../test_data/json_data/' + file_path + '.json'
        with open(self.json_file, 'r') as f:
            return json.loads(f.read())

    @property
    def url(self) -> str:
        url = get_yaml("url")
        url = self.key_is_exist('url').replace("{{ url }}", url)
        return url

    @property
    def method(self) -> str:
        return self.key_is_exist('method')

    @property
    def haders(self) -> dict:
        return self.key_is_exist('headers')

    @property
    def body(self) -> dict:
        return self.key_is_exist('body')

    @property
    def files(self) -> dict:
        files = self.key_is_exist('files')
        if files is not None:
            for key, value in files.items():
                filePath = '../test_data/files/%s' % value
                f = open(filePath, 'rb')
                files[key] = f
        return files

    @property
    def db_config(self) -> dict:
        return self.key_is_exist('db_config')

    @property
    def rely_cases(self) -> dict:
        return self.key_is_exist('rely_cases')

    @property
    def asserts(self) -> dict:
        return self.key_is_exist('asserts')

    @property
    def after(self) -> dict:
        return self.key_is_exist('after')

    def replace_variable(self, replace_variable, replace_value):
        variable = "{{ " + replace_variable + " }}"

        jsonValues = str(self.json_values)
        jsonValues = jsonValues.replace(variable, replace_value)
        self.json_values = eval(jsonValues)
        print(self.json_values)

    def key_is_exist(self, key: str, body: dict = None):

        if body is None:
            body = self.json_values

        try:
            return body[key]
        except KeyError:
            raise KeyError("文件：%s 中缺少必要 Key: %s" % (self.json_file, key))
