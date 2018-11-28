from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic import ListView, DeleteView, UpdateView
from rosreestr.models import ApiRosreestrRequests
from .forms import ConfirmOwnerRequestForm, SendAPIRosreestrRequestForm
from .services import *
from .models import Owner

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

    def get_form_kwargs(self):    # Передадим в форму параметр - помещение, на которое пришел запрос
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
        if not form.instance.rosreestr:
            form.add_error(None, ValidationError('Can not be greater than one'))
            return super(CheckOwnerRequestView, self).form_invalid(form=form)
        #     apirequest = ApiRosreestrRequests(cadastre=form.instance.room.cadastre)
        #     apirequest.save()
        #     if not apirequest.get_object_info():
        #
        #
        #     apirequest.get_encoded_object()
        #     if apirequest.document_available():
        #         if apirequest.place_order():
        #             form.instance.rosreestr = apirequest
        #     messages.success(self.request, 'Запрос в apirosreestr.ru отправлен', 'icon-ok-sign')
        # else:
        #     messages.error(self.request, 'Запрос в росреестр уже отправлялся', 'icon-remove-sign')
        return super(CheckOwnerRequestView, self).form_valid(form=form)



# ======================= Удаление заявки на право собственности на помещение =======================
class DeleteOwnerRequest(DeleteView):
    model = Owner

    def get(self, request, *args, **kwargs):
        return redirect('home')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()   # Попробуем найти объект
        if (not request.user.is_staff) and (request.user != obj.user):   # Если сотрудник или создатель, все гуд
            return HttpResponseForbidden("Недостаточно прав для данного действия")
        return super(DeleteOwnerRequest, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Запрос успешно удален', 'icon-ok-sign')
        return super(DeleteOwnerRequest, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        self.success_url = self.request.POST.get('next', None)
        return super(DeleteOwnerRequest, self).get_success_url()
