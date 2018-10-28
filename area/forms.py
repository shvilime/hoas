from django import forms
from django.db.models import IntegerField
from django.db.models.functions import Cast
from .models import Room, Owner

# ======================= ********************************************** ==========================
class SendOwnerRequestForm(forms.ModelForm):
    room = forms.ModelChoiceField(Room.objects.annotate(room_integer=Cast('number', IntegerField())).order_by('room_integer'))

    class Meta:
        model = Owner
        fields = ['room','portion']

# ======================= ********************************************** ==========================
class ConfirmOwnerRequest(forms.ModelForm):
    request = forms.ModelMultipleChoiceField(queryset=None,
                                             widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        room = kwargs.pop('room')
        self.fields['request'].queryset = Owner.objects.filter(room=room)

    class Meta:
        model = Owner
        fields = ['request']


