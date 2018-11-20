from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View, ListView
from .forms import ConfirmOwnerRequestForm
from .models import Owner
from .services import *


# Create your views here.

# ======================= Просмотр запросов на регистрацию собственности ==========================
class OwnerRequestsView(ListView):
    template_name = 'ownerrequests.html'
    queryset = Owner.objects.filter(date_confirmation=None, date_cancellation=None)
    context_object_name = 'requests'


# ======================= Подтверждение запроса на регистрацию собственности ======================
class ConfirmRequestView(View):
    template_name = 'confirmrequest.html'
    request_id = 0
    new_owner = None

    def dispatch(self, request, *args, **kwargs):
        self.request_id = kwargs.get('id', 0)
        self.new_owner = Owner.objects.get(pk=self.request_id)
        return super(ConfirmRequestView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        confirmform = ConfirmOwnerRequestForm(room=self.new_owner.room)
        return render(request, self.template_name, {'new_owner': self.new_owner,
                                                    'confirmform': confirmform})

    def post(self, request, *args, **kwargs):
        confirmform = ConfirmOwnerRequestForm(request.POST, room=self.new_owner.room)
        if confirmform.is_valid():
            old_owners_portion = previous_owners_portion(self.new_owner)  # Какая доля у предыдущих собственников
            if 'ownerrequest' in request.POST:  # Форма вернула данные об отмеченных прежних владельцах
                list_owners_selected = request.POST.getlist('ownerrequest')  # Собстенники выбранные для анулирования
                selected_owners_portion = list_owners_portion(list_owners_selected)  # Доля у выбранных собственников

                if (selected_owners_portion >= self.new_owner.portion) or (
                        selected_owners_portion == old_owners_portion):
                    cancel_list_owners(list_owners_selected, self.new_owner)  # Анулируем предыдущих владельцев
                    self.new_owner.confirm()  # Подтвердим нового собственника
                    messages.success(request, 'Новый владелец подтвержден', 'icon-ok-sign')
                    return redirect('area:ownerrequests')
                else:  # Ругаемся, на неверный выбор
                    messages.error(request, 'Неправильный выбор владельцев', 'icon-remove-sign')

            else:  # Форма не вернула данных о предыдущих владельцах
                if old_owners_portion == 0:  # Доля прежних собственников нулевая, подтверждаем запрос
                    self.new_owner.confirm()  # Подтвердим нового собственника
                    messages.success(request, 'Новый владелец подтвержден', 'icon-ok-sign')
                    return redirect('area:ownerrequests')
                else:  # Ругаемся, что нужно анулировать предыдущих собственников
                    messages.error(request, 'Необходимо выбрать владельцев', 'icon-remove-sign')

        return render(request, self.template_name, {'new_owner': self.new_owner,
                                                    'confirmform': confirmform})

