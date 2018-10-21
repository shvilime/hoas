from django import forms
from django.db.models import IntegerField
from django.db.models.functions import Cast
from .models import Owner


class SendOwnerRequest(forms.ModelForm):
    room = forms.ModelChoiceField(Owner.objects.annotate(room_integer=Cast('room', IntegerField())).order_by('room_integer', 'room'))

    class Meta:
        model = Owner
        fields = ['room','portion']

