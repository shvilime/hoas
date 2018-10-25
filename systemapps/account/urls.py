from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path
from django.contrib.auth import views as auth_views
from systemapps.account import views as account_views

accounts_urlpatterns = [
    re_path(r'^login/$', account_views.LoginSignupView, name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            account_views.ActivateAccountView, name='activate'),
    re_path(r'^profile/$', login_required(account_views.ProfileView.as_view(),
                                          login_url='account:login'), name='profile'),
    re_path(r'^profile/(?P<activetab>[0-9]{1})/$',
            login_required(account_views.ProfileView.as_view(), login_url='account:login'), name='profile'),
    re_path(r'^deleteowner/$', account_views.deleteOwnerRequest, name='deleteowner'),
]
