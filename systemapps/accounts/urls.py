from django.urls import path, re_path
from django.contrib.auth import views as auth_views

accounts_urlpatterns = [
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
]