from django import forms
from .models import Owner


class SendOwnerRequest(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['room','portion']
