from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import DeleteView
from .models import CounterValue

# Create your views here.


# ======================= Удаление заявки на право собственности на помещение =====================
class DeleteCounterValue(DeleteView):
    model = CounterValue

    def get(self, request, *args, **kwargs):
        return redirect('home')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Показания успешно удалены', 'icon-ok-sign')
        return super(DeleteCounterValue, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        self.success_url = self.request.POST.get('next', None)
        return super(DeleteCounterValue, self).get_success_url()
