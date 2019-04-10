# -- coding: utf-8 --
from requests import Response


class ResponseOper:

    def __init__(self, response: Response):
        response.encoding = 'utf-8'
        self.code = response.status_code
        self.body = response.text
        self.request_url = response.url

    