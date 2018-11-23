from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.views.generic import DeleteView
from .models import CounterValue

# Create your views here.


# ======================= Удаление заявки на право собственности на помещение =====================
class DeleteCounterValue(DeleteView):
    model = CounterValue

    def get(self, request, *args, **kwargs):
        return redirect('home')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()   # Попробуем найти объект
        if (not request.user.is_staff) and (request.user != obj.user):   # Если сотрудник или создатель, все гуд
            return HttpResponseForbidden("Недостаточно прав для данного действия")
        return super(DeleteCounterValue, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Показания успешно удалены', 'icon-ok-sign')
        return super(DeleteCounterValue, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        self.success_url = self.request.POST.get('next', None)
        return super(DeleteCounterValue, self).get_success_url()
