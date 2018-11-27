from django.urls import re_path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from rosreestr import views as rosreestr_views

rosreestr_urlpatterns = [
    re_path(r'^rosreestrnet/$',
            staff_member_required(rosreestr_views.rosreestrnet_getdata, login_url="account:login"),
            name='rosreestrnet'),
    re_path(r'^apirosreestr/$',
            staff_member_required(rosreestr_views.apirosreestr_getdata, login_url="account:login"),
            name='apirosreestr'),
]
