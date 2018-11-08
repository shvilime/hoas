from django import forms
from django.db.models import IntegerField
from django.db.models.functions import Cast
from .models import Room, Owner


# ======================= ********************************************** ==========================
class SendOwnerRequestForm(forms.ModelForm):
    room = forms.ModelChoiceField(label="Номер помещения",
                                  queryset=Room.objects.annotate(
                                      room_integer=Cast('number', IntegerField())).order_by('room_integer')
                                  )
    class Meta:
        model = Owner
        fields = ['room', 'portion']


# ======================= ********************************************** ==========================
class ConfirmOwnerRequestForm(forms.ModelForm):
    ownerrequest = forms.ModelMultipleChoiceField(required=False,
                                                  queryset=None,
                                                  widget=forms.CheckboxSelectMultiple(
                                                      attrs={'class': 'checkbox-style'}))

    def __init__(self, *args, **kwargs):
        room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)
        self.fields['ownerrequest'].queryset = Owner.objects.filter(room=room, date_confirmation__isnull=False)

    class Meta:
        model = Owner
        fields = ['ownerrequest']
