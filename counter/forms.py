from django import forms
from django.core.exceptions import ValidationError
from django.db.models import IntegerField
from django.db.models.functions import Cast
from .services import *
from area.services import *
from area.models import Owner, Room
from .models import CounterValue, CounterType


# =========================== Форма отправки показания счетчика услуг ==============================
class OwnerModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '%s' % obj.room


class SendCounterValueForm(forms.ModelForm):
    room = forms.ModelChoiceField(label="Номер помещения", queryset=None)
    type = forms.ModelChoiceField(label="Тип счетчика", queryset=None)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.room = None
        self.date = datetime.date.today()
        super(SendCounterValueForm, self).__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(number__in=[item.room.number for item in
                                                                       owner_requests_history(self.user, active=True)])
        self.fields['type'].queryset = list_active_counters()

    def clean(self):
        cleaned_data = super(SendCounterValueForm, self).clean()
        # Проверим дату приема показаний
        if not check_actual_counter_period(cleaned_data['type']):
            start, end = get_counter_period(cleaned_data['type'])
            raise ValidationError('Период приема показаний установлен с {0} по {1} число месяца'.format(start, end))
        # Проверим на наличие ранее введенных показаний счетчика
        if not check_value_duplication(cleaned_data['room'], cleaned_data['type'], datetime.date.today()):
            raise ValidationError('Показания счетчика для данного месяца уже существуют')
        # Проверим на приращение счетчика
        if not check_value_increment(cleaned_data['room'], cleaned_data['type'],
                                     datetime.date.today(), cleaned_data['value']):
            raise ValidationError('Показания счетчика должны быть больше чем предыдущее значение')

        return cleaned_data

    class Meta:
        model = CounterValue
        fields = ['room', 'type', 'value']
