from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from .forms import ConfirmOwnerRequestForm
from .models import Owner


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
    popup_message = dict(type='',icon='',message='')

    def dispatch(self, request, *args, **kwargs):
        self.request_id = kwargs.get('id', 0)
        self.new_owner = Owner.objects.get(pk=self.request_id)
        return super(ConfirmRequestView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        confirmform = ConfirmOwnerRequestForm(room=self.new_owner.room)
        return render(request, self.template_name, {'new_owner': self.new_owner,
                                                    'confirmform': confirmform,
                                                    'popup_message': self.popup_message})

    def post(self, request, *args, **kwargs):
        confirmform = ConfirmOwnerRequestForm(request.POST, room=self.new_owner.room)
        if confirmform.is_valid():
            if 'ownerrequest' in request.POST:  # Переданы данные для аннулирования прежних владельце
                owners4cancel = request.POST.getlist('ownerrequest')
                for owner_id in owners4cancel:
                    Owner.objects.get(pk=owner_id).cancel()
                self.new_owner.confirm()
            else:  # Нет данных о предыдущих владельцах
                self.new_owner.confirm()
            return redirect('area:ownerrequests')
        else:
            self.popup_message={'type': 'error',
                                'icon': 'icon-remove-sign',
                                'message': 'Необходимо выбрать значения'}

        return render(request, self.template_name, {'new_owner': self.new_owner,
                                                    'confirmform': confirmform,
                                                    'popup_message': self.popup_message})
