# -- coding: utf-8 --
import requests

re = requests.Session()

class HttpRequestUtils:
    """
    http 接口请求类
    """

    @staticmethod
    def run(method: str, url, *args, **kwargs):
        method = method.upper()
        print("Method : %r" % method)
        print("URL: %r" % url)
        _result = None
        if method == 'GET':
            _result = re.get(url=url, **kwargs)
        elif method == 'POST':
            print('headers: %r' % kwargs['headers'])
            # print('body: %r' % kwargs['data'])
            _result = re.post(url=url,  *args, **kwargs)

        elif method == 'PUT':
            _result = re.put(url=url, *args, **kwargs)
        elif method == 'DEL' or method == 'DELETE':
            _result = re.delete(url=url, **kwargs)

        _result.encoding = 'unicode_escape'

        print("Response text: %r " % _result.text)

        print('----------------------------------------------------')
        return _result


if __name__ == '__main__':
    result = re.post(
        url='http://daily.qianou.com/member/butler_login.do',
        data={"mobile": "SDGKA72", "password": "sdg123"},
        headers={"content-type":"application/json"}
    )

    print(result.text)