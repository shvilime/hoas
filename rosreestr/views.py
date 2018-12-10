from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from decouple import config
from django.views.generic import View
from .rosreestrnet import ClientRosreestrNet
from .models import ApiRosreestrRequests


# Create your views here.
# ==================== Получить данные с rosreestr.net и вернуть их в JSON ==========================
def rosreestrnet_getdata(request):
    if request.method == 'POST':
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
        self.id = kwargs.get('pk', None)
        return super(ShowXMLView, self).dispatch(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        apirequest = ApiRosreestrRequests.objects.get(pk=self.id)
        xml = apirequest.xml_file.encode()
        return HttpResponse(xml, content_type='text/xsl; charset=utf-8')


# ================== Обработать Hook с apirosreestr.ru и изменить статус запроса ====================
class HookEventView(View):
    key = None
    data = None
    
    def dispatch(self, request, *args, **kwargs):
        self.key = request.POST.get('secret_key', None)
        self.data = request.POST.getlist('data', None)
        return super(HookEventView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden("Отправка данных возможна только методом POST")

    def post(self, request, *args, **kwargs):
        if self.key and self.key == config('HOOK_KEY'):
            rosreestr = ApiRosreestrRequests.objects.get(invoice=self.data['transaction_id'])
            rosreestr.update_order_info()
        return HttpResponse('OK')
