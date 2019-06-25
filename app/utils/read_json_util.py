# -- coding: utf-8 --
import json
from app.utils.common_util import getYaml


class ReadJsonUtils:
    jsonValues = None

    def __init__(self, filePath: str):
        self.jsonValues = self.read_json(filePath)

    def read_json(self, filePath: str) -> dict:

        '''
        读取 json 文件
        :param file_name: 文件名称 ，支持： login/login.json
        '''
        self.json_file = '../test_data/json_data/' + filePath + '.json'
        with open(self.json_file, 'r') as f:
            return json.loads(f.read())

    @property
    def url(self) -> str:
        url = getYaml("url")
        url = self._keyIsExist('url').replace("{{ url }}", url)
        return url

    @property
    def method(self) -> str:
        return self._keyIsExist('method')

    @property
    def haders(self) -> dict:
        return self._keyIsExist('headers')

    @property
    def body(self) -> dict:
        return self._keyIsExist('body')

    @property
    def files(self) -> dict:
        files = self._keyIsExist('files')
        if files is not None:
            for key, value in files.items():
                filePath = '../test_data/files/%s' % value
                f = open(filePath, 'rb')
                files[key] = f
        return files

    @property
    def rely_cases(self) -> dict:
        return self._keyIsExist('rely_cases')

    @property
    def asserts(self) -> dict:
        return self._keyIsExist('asserts')

    @property
    def after(self) -> dict:
        return self._keyIsExist('after')

    def replaceVariable(self, replace_variable, replace_value):
        variable = "{{ " + replace_variable + " }}"

        jsonValues = str(self.jsonValues)
        jsonValues = jsonValues.replace(variable, replace_value)
        self.jsonValues = eval(jsonValues)
        print(self.jsonValues)

    def _keyIsExist(self, key: str):
        try:
            return self.jsonValues[key]
        except KeyError:
            raise KeyError("文件：%s 中缺少必要 Key: %s" % (self.json_file, key))
