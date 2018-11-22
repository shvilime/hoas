from django.urls import re_path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from counter import views as counter_views

counter_urlpatterns = [
    re_path(r'^deletevalue/(?P<pk>\d+)/$', login_required(counter_views.DeleteCounterValue.as_view(),
                                                          login_url='account:login'), name='deletevalue'),
]
