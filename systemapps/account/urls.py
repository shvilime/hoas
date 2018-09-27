from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from systemapps.account import views as account_views

accounts_urlpatterns = [
    re_path(r'^login/$', account_views.LoginSignupView, name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            account_views.ActivateAccountView, name='activate'),
]