from django.urls import path, re_path
from django.utils.http import is_safe_url
from django.shortcuts import redirect
from django.conf import settings

from main.views import home

main_urlpatterns = [
    re_path('^$', home, name='home'),
]


def redirect_next(request):
    next_url = request.POST.get('next', None)
    # Checking the next URL and redirect
    url_is_safe = is_safe_url(url=next_url, allowed_hosts=settings.ALLOWED_HOSTS,
                              require_https=request.is_secure())
    if next_url and url_is_safe:
        return redirect(next_url)
    else:
        return redirect('home')
