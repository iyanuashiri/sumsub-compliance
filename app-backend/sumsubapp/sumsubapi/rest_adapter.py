import hashlib
import hmac
import time
from json import JSONDecodeError
from typing import Dict

from requests import Session
from requests import RequestException

from .exceptions import SumsubError
from .models import Response


class Rest:
    def __init__(self, app_token, secret_key, base_url: str = 'https://api.sumsub.com'):
        """
        :param app_token:
        :param secret_key:

        """
        self.app_token = app_token
        self.secret_key = secret_key
        self.base_url = base_url
        self.session = Session()

        now = int(time.time())
        prepared_request = request.prepare()
        method = request.method.upper()
        path_url = prepared_request.path_url
        body = b'' if prepared_request.body is None else prepared_request.body
        data_to_sign = str(now).encode('utf-8') + method.encode('utf-8') + path_url.encode('utf-8') + body

        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            data_to_sign,
            digestmod=hashlib.sha256
        )

        self.headers = {'Content-Type': 'application/json', 'X-App-Token': self.app_token,
                        'X-App-Access-Sig': signature, 'X-App-Access-Ts': str(now),
                        "X-Return-Doc-Warnings": "true",
                        }

    def _request(self, http_method: str, endpoint: str, params: Dict = None, body: Dict = None):
        """
        :param http_method:
        :param endpoint:
        :param params:
        :param body:
        :return:
        """
        full_url = self.base_url + endpoint
        try:
            response = self.session.request(method=http_method, url=full_url, headers=self.headers, params=params,
                                            data=body)
        except RequestException as e:
            raise SumsubError(message=e.response)

        try:
            data = response.json()
        except (ValueError, JSONDecodeError) as e:
            raise SumsubError(message=e)

        if 299 >= response.status_code >= 200:
            return Response(response.status_code, data=data)
        raise SumsubError(message=response.reason, status_code=response.status_code)

    def get(self, endpoint: str, params: Dict = None):
        """
        :param endpoint:
        :param params:
        :return:
        """
        return self._request(http_method='get', endpoint=endpoint, params=params)

    def post(self, endpoint: str, params: Dict = None, data: Dict = None):
        """
        :param endpoint:
        :param params:
        :param data:
        :return:
        """
        return self._request(http_method='post', endpoint=endpoint, params=params, body=data)