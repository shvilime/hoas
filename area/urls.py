from django.urls import re_path
from django.contrib.admin.views.decorators import staff_member_required
from area import views as area_views

area_urlpatterns = [
    re_path(r'^ownerrequests/$', staff_member_required(area_views.OwnerRequestsView.as_view(),
                                                       login_url="account:login"), name='ownerrequests'),
]
