from django.shortcuts import render
from django.http import JsonResponse
from decouple import config
from .rosreestrapi import Client


# Create your views here.


def rosreestr_getdata(request):
    egrn = request.POST.get('egrn', False)
    client = Client(token=config('ROSREESTR_KEY'))
    data = client.post(method='database.get', result='owners', egrn=egrn)
    return JsonResponse(data, safe=False)
