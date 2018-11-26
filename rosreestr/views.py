from django.shortcuts import render
from django.http import JsonResponse
from decouple import config
from .rosreestrnet import ClientRosreestrNet


# Create your views here.


def rosreestr_getdata(request):
    egrn = request.POST.get('egrn', False)
    client = ClientRosreestrNet(token=config('ROSREESTRNET_KEY'))
    client.post(method='database.reload', egrn=egrn)
    client.post(method='database.get', result='owners', egrn=egrn)
    return JsonResponse(client.response, safe=False)
