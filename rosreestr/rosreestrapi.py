import json
import xmltodict
import xml.etree.cElementTree as ET
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError


# ===================================================================
class ClientApiRosreestr:
    token = ''
    url = 'http://apirosreestr.ru/api/'
    api_method = ''
    result_key = ''
    accepted_method = list()
    params = dict()
    response = dict()
    error_code = 0
    error = ''

    def __init__(self, token):
        self.token = token

    def find(self, key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in self.find(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in self.find(key, d):
                        yield result

    def set_access_params(self):  # Установим необходимые параметры запроса
        self.params.pop('method', None)  # Очистим от лишнего параметра
        self.params.pop('result', None)  # Очистим от лишнего параметра

    def post_request(self):
        self.set_access_params()
        self.error = ''
        self.error_code = 0
        headers = {'Token': self.token}
        params = urlencode(self.params).encode()  # Перекодируем параметры в строку параметров запроса
        # params = bytes(json.dumps(self.params), encoding="utf-8")
        request = Request(url=self.url + self.api_method, data=params,
                          headers=headers)  # Сформируем полную строку запроса
        try:
            response = urlopen(request)  # Попытаемся открыть строку запроса
        except URLError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
        else:
            return response.read().decode()

    @staticmethod
    def is_json(any_string):
        try:
            json.loads(any_string)
        except ValueError:
            return False
        return True

    @staticmethod
    def is_xml(any_string):
        try:
            ET.fromstring(any_string)
        except ET.ParseError:
            return False
        return True

    def check_result(self, any_string):
        if self.is_json(any_string):
            parsed_json = json.loads(any_string)
            if parsed_json['error']:
                self.error_code = parsed_json['error']['code']
                self.error = parsed_json['error']['mess']
                return False
            else:
                self.response = parsed_json
                return True
        if self.is_xml(any_string):
            self.response = any_string
            return True

    def get_data(self, **kwargs):
        self.params = kwargs
        if self.api_method not in self.accepted_method:
            raise ValueError('Метод должен быть из числа: ' + str(self.accepted_method))
        if self.check_result(self.post_request()):
            try:
                return self.response[self.result_key]
            except:
                return self.response
        else:
            return ''

    # ============================= Вызываемые методы для получения данных ======================================
    def post(self, method='', result='', **kwargs):
        self.accepted_method = (
            'cadaster/objectInfoFull', 'cadaster/Save_order', 'cadaster/orders', 'cadaster/download',
            'cadaster/search','transaction/info', 'transaction/pay')
        self.api_method = method
        self.result_key = result
        return self.get_data(**kwargs)
