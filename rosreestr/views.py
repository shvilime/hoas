from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseForbidden
from decouple import config
from .rosreestrnet import ClientRosreestrNet
from .models import ApiRosreestrRequests


# Create your views here.


def rosreestrnet_getdata(request):
    if request.method=='POST':
        egrn = request.POST.get('egrn', '')
        client = ClientRosreestrNet(token=config('ROSREESTRNET_KEY'))
        client.post(method='database.reload', egrn=egrn)
        client.post(method='database.get', result='owners', egrn=egrn)
        return JsonResponse(client.response, safe=False)
    else:
        return HttpResponseForbidden("Запрос данных возможно только методом POST")


def apirosreestr_getdata(request):
    # egrn = request.POST.get('egrn', '')
    # next = request.POST.get('next')
    # apirequest = ApiRosreestrRequests(cadastre=egrn)
    # apirequest.save()
    # apirequest.get_object_info()
    # apirequest.get_encoded_object()
    # apirequest.document_available()

    # clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
    # clientapi.post(method='cadaster/objectInfoFull', result='encoded_object', query=egrn)
    # if clientapi.response['documents']['XZP']['available'] == True:
    #     return

    return redirect('area:ownerrequests')