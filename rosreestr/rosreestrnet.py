import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError


# ===================================================================
class ClientRosreestrNet:
    token = ''
    url = 'https://rosreestr.net/api/method/'
    api_version = '1.0'
    api_format = 'json'
    api_method = ''
    result_key = ''
    accepted_method = list()
    params = dict()
    response = dict()
    error_code = 0
    error = ''

    def __init__(self, token):
        self.token = token

    def set_access_params(self):  # Установим необходимые параметры запроса
        self.params['v'] = self.api_version
        self.params['access_token'] = self.token
        self.params['format'] = self.api_format
        self.params.pop('method', None)  # Очистим от лишнего параметра
        self.params.pop('result', None)  # Очистим от лишнего параметра

    def post_request(self):
        self.set_access_params()
        params = urlencode(self.params).encode()  # Перекодируем параметры в строку параметров запроса
        request = Request(self.url + self.api_method, params)  # Сформируем полную строку запроса
        try:
            response = urlopen(request)  # Попытаемся открыть строку запроса
        except URLError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
        else:
            return response.read().decode()

    def check_result(self, json_string):
        parsed_json = json.loads(json_string)
        if 'response' in parsed_json:
            self.response = parsed_json['response']['data']
            return True
        if 'error' in parsed_json:
            self.error_code = parsed_json['error']['error_code']
            self.error = parsed_json['error']['error_msg']
            return False

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
    def post(self, method='account.info', result='balance', **kwargs):
        self.accepted_method = ('account.info', 'service.getByEgrn', 'database.get', 'database.reload')
        self.api_method = method
        self.result_key = result
        return self.get_data(**kwargs)
