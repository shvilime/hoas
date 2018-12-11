import re
from rosreestr.rosreestrapi import ClientApiRosreestr
from decouple import config

#================================================================================================
def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

#================================================================================================
def FillAreasInitial():
    clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
    listapp = clientapi.post(method='cadaster/search',
                             query="Краснодар, Зиповская улица, д.3/3",
                             grouped=0)
    for flat in listapp['objects']:
        flatnumber = re.search('кв[\. ]{0,}(\d+(?:[\.,]\d+)?)', flat['ADDRESS']).group(1)
        cadastre = flat['CADNOMER']
        square = re.search('\d+(?:[\.,]\d+)?', flat['AREA']).group(0)




    return True