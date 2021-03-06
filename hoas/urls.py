"""hoas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

from main.urls import main_urlpatterns
from systemapps.account.urls import accounts_urlpatterns
from area.urls import area_urlpatterns
from counter.urls import counter_urlpatterns
from rosreestr.urls import rosreestr_urlpatterns
from voting.urls import voting_urlpatterns

urlpatterns = [
    re_path('^', include(main_urlpatterns)),
    re_path('^account/', include((accounts_urlpatterns,'account'), namespace='account')),
    re_path('^area/', include((area_urlpatterns,'area'), namespace='area')),
    re_path('^counter/', include((counter_urlpatterns, 'counter'), namespace='counter')),
    re_path('^rosreestr/', include((rosreestr_urlpatterns, 'rosreestr'), namespace='rosreestr')),
    re_path('^voting/', include((voting_urlpatterns, 'voting'), namespace='voting')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)