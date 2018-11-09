import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError


# ===================================================================
class Client:
    token = ''
    url = 'https://rosreestr.net/api/method/'
    api_version = '1.0'
    api_format = 'json'
    api_method = ''
    accepted_method = list()
    params = dict()
    response = dict()
    error_code = 0
    error = ''

    def __init__(self, token):
        self.token = token

    def set_access_params(self):
        self.params['v'] = self.api_version
        self.params['access_token'] = self.token
        self.params['format'] = self.api_format
        self.params.pop('method', None)   # Очистим от лишнего параметра
        self.params.pop('result', None)   # Очистим от лишнего параметра

    def post_request(self):
        self.set_access_params()
        params = urlencode(self.params).encode()    # Перекодируем параметры в строку запроса
        request = Request(self.url + self.api_method, params)
        try:
            response = urlopen(request)
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
        if kwargs['method'] not in self.accepted_method:
            raise ValueError('Метод должен быть из числа: ' + str(self.accepted_method))
        if self.check_result(self.post_request()):
            return self.response[kwargs['result']]
        else:
            return ''

    def account(self, **kwargs):
        self.accepted_method = ('info',)
        self.api_method = 'account.' + kwargs['method']
        return self.get_data(**kwargs)
