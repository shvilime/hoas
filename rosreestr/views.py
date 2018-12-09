from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from decouple import config
from django.views.generic import View
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


# ======================= Показать выписку, полученную из росреестра ================================
class ShowXMLView(View):
    id = None

    def dispatch(self, request, *args, **kwargs):
        self.id = kwargs.get('pk',None)
        return super(ShowXMLView, self).dispatch(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        apirequest = ApiRosreestrRequests.objects.get(pk=self.id)
        xml = apirequest.xml_file.encode()
        return HttpResponse(xml, content_type='text/xsl; charset=utf-8')


