from django.urls import re_path
from area import views as area_views

area_urlpatterns = [
    re_path(r'^ownerrequests/$', area_views.OwnerRequestsView, name='ownerrequests'),
]
