from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.views.generic import View, ListView, DeleteView, UpdateView
from main.urls import redirect_next
from .forms import ConfirmOwnerRequestForm
from .services import *
from .models import Owner


# Create your views here.

# =================== Просмотр списка запросов на регистрацию собственности =======================
class ListOwnerRequestView(ListView):
    template_name = 'ownerrequests.html'
    queryset = Owner.objects.filter(date_confirmation=None, date_cancellation=None)
    context_object_name = 'requests'


# ======================= Подтверждение запроса на регистрацию собственности ======================
class _OwnerRequestView(UpdateView):
    template_name = 'confirmrequest.html'
    model = Owner
    context_object_name = 'new_owner'
    form_class = ConfirmOwnerRequestForm

    def get_form_kwargs(self):    # Передадим в форму параметр - помещение, на которое пришел запрос
        kwargs = super(_OwnerRequestView, self).get_form_kwargs()
        kwargs['room'] = self.get_object().room
        return kwargs







class OwnerRequestView(View):
    template_name = 'confirmrequest.html'
    owner_request = None

    def dispatch(self, request, *args, **kwargs):
        self.owner_request = Owner.objects.get(pk=kwargs.get('pk'))
        return super(OwnerRequestView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        confirmform = ConfirmOwnerRequestForm(room=self.owner_request.room)
        return render(request, self.template_name, {'new_owner': self.owner_request,
                                                    'form': confirmform})

    def post(self, request, *args, **kwargs):
        confirmform = ConfirmOwnerRequestForm(request.POST, room=self.owner_request.room)
        if confirmform.is_valid():
            old_owners_portion = previous_owners_portion(self.owner_request)  # Какая доля у предыдущих собственников
            if 'ownerrequest' in request.POST:  # Форма вернула данные об отмеченных прежних владельцах
                list_owners_selected = request.POST.getlist('ownerrequest')  # Собстенники выбранные для анулирования
                selected_owners_portion = list_owners_portion(list_owners_selected)  # Доля у выбранных собственников

                if (selected_owners_portion >= self.owner_request.portion) or (
                        selected_owners_portion == old_owners_portion):
                    cancel_list_owners(list_owners_selected, self.owner_request)  # Анулируем предыдущих владельцев
                    self.owner_request.confirm()  # Подтвердим нового собственника
                    messages.success(request, 'Новый владелец подтвержден', 'icon-ok-sign')
                    return redirect('area:ownerrequests')
                else:  # Ругаемся, на неверный выбор
                    messages.error(request, 'Неправильный выбор владельцев', 'icon-remove-sign')

            else:  # Форма не вернула данных о предыдущих владельцах
                if old_owners_portion == 0:  # Доля прежних собственников нулевая, подтверждаем запрос
                    self.owner_request.confirm()  # Подтвердим нового собственника
                    messages.success(request, 'Новый владелец подтвержден', 'icon-ok-sign')
                    return redirect('area:ownerrequests')
                else:  # Ругаемся, что нужно анулировать предыдущих собственников
                    messages.error(request, 'Необходимо выбрать владельцев', 'icon-remove-sign')

        return render(request, self.template_name, {'new_owner': self.owner_request,
                                                    'form': confirmform})


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
