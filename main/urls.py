from django.urls import path, re_path

from main.views import home

main_urlpatterns = [
    re_path('^$', home, name='home'),
]