from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from decouple import config
from django.views.generic import View
from .rosreestrnet import ClientRosreestrNet
from .services import GetListAreasFromAddress, GetAreaInfo
from .models import ApiRosreestrRequests


# Create your views here.
# ==================== Получить данные с rosreestr.net и вернуть их в JSON ==========================
class RosreestrNet_GetData(View):
    egrn = ''
    
    def dispatch(self, request, *args, **kwargs):
        self.egrn = request.POST.get('egrn', '')
        return super(RosreestrNet_GetData, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden("Запрос данных возможно только методом POST")

    def post(self, request, *args, **kwargs):
        client = ClientRosreestrNet(token=config('ROSREESTRNET_KEY'))
        client.post(method='database.reload', egrn=self.egrn)
        client.post(method='database.get', result='owners', egrn=self.egrn)
        return JsonResponse(client.response, safe=False)
    

# =================== Получить данные с apirosreestr.ru и вернуть их в JSON =========================
class ApiRosreestr_GetData(View):
    cadastre = ''

    def dispatch(self, request, *args, **kwargs):
        self.cadastre = request.POST.get('cadastre', '')
        return super(ApiRosreestr_GetData, self).dispatch(request, args, kwargs)
    
    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden("Запрос данных возможно только методом POST")

    def post(self, request, *args, **kwargs):
        response = dict()
        if not request.user.is_superuser:
            return HttpResponseForbidden("Получать данные может только администратор")
        if not self.cadastre:
            response = GetListAreasFromAddress('Краснодар, Зиповская улица, д.3/3')
        else:
            response = GetAreaInfo(self.cadastre)
        return JsonResponse(response, safe=False)


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
    invoice_id = None
    
    def dispatch(self, request, *args, **kwargs):
        self.key = request.POST.get('secret_key', None)
        self.invoice_id = request.POST.get('data[transaction_id]', None)
        return super(HookEventView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden("Отправка данных возможна только методом POST")

    def post(self, request, *args, **kwargs):
        if self.key and self.key == config('HOOK_KEY'):
            rosreestr = ApiRosreestrRequests.objects.get(invoice=self.invoice_id)
            rosreestr.update_order_info()
            rosreestr.check_owner(username=request.user.fullname.upper())
            rosreestr.download_file()
        return HttpResponse('OK')
