import re
from rosreestr.rosreestrapi import ClientApiRosreestr
from decouple import config


# ================================================================================================
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


# ================================================================================================
def GetListAreasFromAddress(address=''):
    clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
    listareas = clientapi.post(method='cadaster/search', query=address,
                               grouped=0)
    return listareas


def GetAreaInfo(cadastre=''):
    result = list()
    clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
    fullinfo = clientapi.post(method='cadaster/objectInfoFull', query=cadastre, result='EGRN')
    flatnumber = ''
    square = 0
    if not clientapi.error:
        status = fullinfo['details']['Статус объекта'].upper()
        if status == 'УЧТЕННЫЙ' or status == 'РАНЕЕ УЧТЕННЫЙ':
            square = fullinfo['details']["Площадь ОКС'а"]
            search = re.findall('\d+', fullinfo['object']['ADDRESS'])
            if search:
                flatnumber = search[-1]
                result.append((flatnumber, cadastre, square))
    return result
