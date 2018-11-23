from django.urls import re_path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from area import views as area_views

area_urlpatterns = [
    re_path(r'^ownerrequests/$',
            staff_member_required(area_views.ListOwnerRequestView.as_view(), login_url="account:login"),
            name='ownerrequests'),
    re_path(r'^ownerrequests/(?P<pk>\d+)/$',
            staff_member_required(area_views._OwnerRequestView.as_view(), login_url="account:login"),
            name='ownerrequests'),
    re_path(r'^deleteowner/(?P<pk>\d+)/$',
            login_required(area_views.DeleteOwnerRequest.as_view(), login_url='account:login'),
            name='deleteowner'),
]
