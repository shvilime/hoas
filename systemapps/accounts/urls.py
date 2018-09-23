from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from systemapps.accounts import views as account_views

accounts_urlpatterns = [
    re_path(r'^login/$', account_views.loginsignup, name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
]