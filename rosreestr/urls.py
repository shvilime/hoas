from django.urls import re_path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from rosreestr import views as rosreestr_views

rosreestr_urlpatterns = [
    re_path(r'^data/$',
            staff_member_required(rosreestr_views.rosreestr_getdata, login_url="account:login"),
            name='data'),
]
