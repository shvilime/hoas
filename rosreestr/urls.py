from django.urls import re_path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from rosreestr import views as rosreestr_views

rosreestr_urlpatterns = [
    re_path(r'^rosreestrnet/$',
            staff_member_required(rosreestr_views.rosreestrnet_getdata, login_url="account:login"),
            name='rosreestrnet'),
    re_path(r'^showxml/(?P<pk>\d+)/$',
            staff_member_required(rosreestr_views.ShowXMLView.as_view(), login_url="account:login"),
            name='showxml'),
    re_path(r'^hookevent/$',
            rosreestr_views.HookEventView.as_view(),
            name='hookevent'),
]
