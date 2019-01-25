from django import forms
from django.core.exceptions import ValidationError
from .models import Candidate


class AddCandidateForm(forms.ModelForm):
    candidate = forms.CharField(label='Фамилия Имя Отчество',
                                required=True,
                                help_text='Ф.И.О. должно точно совпадать с данными одного из жильцов дома. \
                                           При любом несовпадении кандидатура не будет добавлена')
    class Meta:
        model = Candidate
        fields = ['candidate']

    def clean(self):
        cleaned_data = super(AddCandidateForm, self).clean()
        if cleaned_data['room'] in [item.room for item in owner_requests_history(self.user)]:  # Дубликат запроса
            raise ValidationError('Невозможно добавить данного кандидата')
        return cleaned_data
