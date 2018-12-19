import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic import View, TemplateView, ListView, DeleteView, UpdateView
from rosreestr.models import ApiRosreestrRequests
from .forms import ConfirmOwnerRequestForm, SendAPIRosreestrRequestForm
from .services import *
from .models import Owner, Room


# Create your views here.

# =================== Просмотр списка запросов на регистрацию собственности =======================
class ListOwnerRequestView(ListView):
    template_name = 'ownerrequests.html'
    queryset = Owner.objects.filter(date_confirmation=None, date_cancellation=None)
    context_object_name = 'requests'


# ======================= Подтверждение запроса на регистрацию собственности ======================
class OwnerRequestView(UpdateView):
    template_name = 'confirmrequest.html'
    model = Owner
    context_object_name = 'new_owner'
    form_class = ConfirmOwnerRequestForm
    success_url = reverse_lazy('area:ownerrequests')

    def get_form_kwargs(self):  # Передадим в форму параметр - помещение, на которое пришел запрос
        kwargs = super(OwnerRequestView, self).get_form_kwargs()
        kwargs['room'] = self.get_object().room
        return kwargs

    def form_valid(self, form):
        cancel_list_owners(form.cleaned_data['ownerrequest'], form.instance)  # Анулируем предыдущих владельцев
        form.instance.confirm()  # Подтвердим нового собственника
        messages.success(self.request, 'Новый владелец подтвержден', 'icon-ok-sign')
        return super(OwnerRequestView, self).form_valid(form=form)


# ============================== Проверка запроса по данным росреестра ==============================
class CheckOwnerRequestView(UpdateView):
    template_name = 'checkrequest.html'
    model = Owner
    context_object_name = 'new_owner'
    form_class = SendAPIRosreestrRequestForm
    success_url = reverse_lazy('area:ownerrequests')

    def form_valid(self, form):
        if form.instance.rosreestr:     # Если к заявке на собственность уже привязан запрос, то работаем с ним
            apirequest = ApiRosreestrRequests.objects.get(pk=form.instance.rosreestr.id)
        else:                           # Иначе создать новый запрос или получить созданный, но непривязанный
            apirequest, created = ApiRosreestrRequests.objects.get_or_create(cadastre=form.instance.room.cadastre,
                                                                             date_request__date=datetime.date.today())

        if not apirequest.get_object_info():
            form.add_error(None, ValidationError('Не удалось получить информацию о данном объекте'))
            return super(CheckOwnerRequestView, self).form_invalid(form=form)
        if not apirequest.document_available():
            form.add_error(None, ValidationError('Для данного объекта запрос выписки недоступен'))
            return super(CheckOwnerRequestView, self).form_invalid(form=form)
        if not apirequest.place_order():
            form.add_error(None, ValidationError('Не удалось разместить заказ выписки'))
            return super(CheckOwnerRequestView, self).form_invalid(form=form)
        if not apirequest.update_invoice_info():
            form.add_error(None, ValidationError('Не удалось получить информацию о состоянии инвойса'))
            return super(CheckOwnerRequestView, self).form_invalid(form=form)
        if not apirequest.is_paid and not apirequest.pay_invoice():
            form.add_error(None, ValidationError('Не удалось оплатить заказ'))
            return super(CheckOwnerRequestView, self).form_invalid(form=form)

        # !!!!!!!!!!!!!!!!!!! Удалить потом эти три строчки
        apirequest.update_order_info()
        apirequest.download_file()
        apirequest.check_owner(username=form.instance.user.get_full_name().upper())

        form.instance.rosreestr = apirequest
        messages.success(self.request, 'Запрос в apirosreestr.ru отправлен', 'icon-ok-sign')
        return super(CheckOwnerRequestView, self).form_valid(form=form)


# ======================= Удаление заявки на право собственности на помещение =======================
class DeleteOwnerRequest(DeleteView):
    model = Owner

    def get(self, request, *args, **kwargs):
        return redirect('home')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()  # Попробуем найти объект
        if (not request.user.is_staff) and (request.user != obj.user):  # Если сотрудник или создатель, все гуд
            return HttpResponseForbidden("Недостаточно прав для данного действия")
        return super(DeleteOwnerRequest, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Запрос успешно удален', 'icon-ok-sign')
        return super(DeleteOwnerRequest, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        self.success_url = self.request.POST.get('next', None)
        return super(DeleteOwnerRequest, self).get_success_url()


# ============== Показать страницу заполнения помещений первоначальными значениями ==================
class InitializationView(TemplateView):
    template_name = 'initialization.html'

# =================== Добавить помещение по переданным первоначальным значениям =====================
class AddAreaView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Недостаточно прав для данного действия")
        return super(AddAreaView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden("Добавление помещения возможно только методом POST")

    def post(self, request, *args, **kwargs):
        room = Room(number=request.POST.get('number', None),
                    cadastre=request.POST.get('cadastre', None),
                    square=request.POST.get('square', 0), type='FL')
        room.save()
        return JsonResponse('OK', safe=False)
