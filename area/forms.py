from django import forms
from django.core.exceptions import ValidationError
from django.db.models import IntegerField
from django.db.models.functions import Cast
from .services import *
from .models import Room, Owner


# ======================== Форма отправки запроса прав на помещения  ============================
class SendOwnerRequestForm(forms.ModelForm):
    room = forms.ModelChoiceField(label="Номер помещения",
                                  queryset=Room.objects.annotate(
                                      room_integer=Cast('number', IntegerField())).order_by('room_integer')
                                  )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SendOwnerRequestForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SendOwnerRequestForm, self).clean()
        if cleaned_data['room'] in [item.room for item in owner_requests_history(self.user)]:  # Дубликат запроса
            raise ValidationError('Запрос от пользователя на данное помещение уже существует')
        return cleaned_data

    class Meta:
        model = Owner
        fields = ['room', 'portion']


# =========================== Форма подтверждения прав на помещение =============================
class ConfirmOwnerRequestForm(forms.ModelForm):
    ownerrequest = forms.ModelMultipleChoiceField(required=False,
                                                  queryset=None,
                                                  widget=forms.CheckboxSelectMultiple(
                                                      attrs={'class': 'checkbox-style'}))

    def clean(self):
        cleaned_data = super(ConfirmOwnerRequestForm, self).clean()
        selected_owners_portion = cleaned_data['ownerrequest'].aggregate(summa=Sum('portion'))['summa'] or 0 # Доля у выбранных собственников
        old_owners_portion = previous_owners_portion(self.instance)  # Какая доля у предыдущих собственников

        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)
        self.fields['ownerrequest'].queryset = Owner.objects.filter(room=self.room, date_confirmation__isnull=False)

    class Meta:
        model = Owner
        fields = ['ownerrequest']
