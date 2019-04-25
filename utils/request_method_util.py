# -- coding: utf-8 --
import requests

re = requests.session()


class RequestMethodUtil:
    """
    http 接口请求类
    """

    def __get(self, url: str):
        """
        Get 请求
        :param url: 请求的 URL
        :return: 响应结果
        """
        return re.get(url)

    def __post(self, url: str, headers: dict, body, **kwargs):
        """
        Post 请求
        :param url: 请求的 URL
        :return: 响应结果
        """
        content_type = headers['content-type']
        if not content_type == 'application/json':
            return re.post(url=url, headers=headers, data=body, **kwargs)
        return re.post(url=url, headers=headers, json=body, **kwargs)

    def __put(self, url: str, headers: dict, body, **kwargs):
        """
        Put 请求
        :param url: 请求的 URL
        :return: 响应结果
        """
        content_type = headers['content-type']
        if not content_type == 'application/json':
            return re.put(url=url, headers=headers, data=body, **kwargs)
        return re.put(url=url, headers=headers, json=body, **kwargs)

    def __del(self, url: str, **kwargs):
        """
        Delete 请求
        :param url: 请求的 URL
        :return: 响应结果
        """
        return re.delete(url=url, **kwargs)

    def run(self, method: str, url: str, headers: dict = None, body=None):
        """
        同一调取http请求的方法
        :param body: 请求数据
        :param headers: 请求头
        :param method: 请求方式
        :param url: 请求的 URL
        :return: 响应结果
        """
        method = method.lower()
        _result = None
        if method == 'get':
            _result = self.__get(url=url)
        elif method == 'post':
            _result = self.__post(url=url, headers=headers, body=body)
        elif method == 'put':
            _result = self.__put(url=url, headers=headers, body=body)
        elif method == 'del' or method == 'delete':
            _result = self.__del(url=url)
        return _result
