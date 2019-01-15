from django.urls import re_path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from voting import views as voting_views

voting_urlpatterns = [
    re_path(r'^questions/$',
            login_required(voting_views.ListQuestion4VotingView.as_view(), login_url='account:login'),
            name='questions'),
]
