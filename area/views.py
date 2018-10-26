from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Owner

# Create your views here.

# ======================= Просмотр запросов на регистрацию собственности ==========================
class OwnerRequestsView(ListView):
    template_name = 'ownerrequests.html'
    queryset = Owner.objects.filter(date_confirmation=None,date_cancellation=None)
    context_object_name = 'requests'