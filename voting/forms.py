from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Question, Candidate
from area.services import check_user_status_as_owner


class AddCandidateForm(forms.ModelForm):
    question = forms.ModelChoiceField(queryset=Question.objects.all(),
                                      widget=forms.HiddenInput()
                                      )
    nominator = forms.ModelChoiceField(queryset=get_user_model().objects.all(),
                                       widget=forms.HiddenInput()
                                       )
    user = forms.ModelChoiceField(required=False,
                                  queryset=get_user_model().objects.all(),
                                  widget=forms.HiddenInput()
                                  )
    candidate = forms.CharField(label='Фамилия Имя Отчество',
                                required=True,
                                help_text='Ф.И.О. должно точно совпадать с данными одного из жильцов дома. \
                                           При любом несовпадении кандидатура не будет добавлена')

    class Meta:
        model = Candidate
        fields = ['candidate', 'question', 'nominator', 'user']

    def clean(self):
        cleaned_data = super(AddCandidateForm, self).clean()
        model = get_user_model()
        try:                        # Проверим, существует ли пользователь
            owner = model.objects.get(fullname__icontains=cleaned_data['candidate'])
        except model.DoesNotExist:
            raise ValidationError('Кандидат не найден')

        if Candidate.objects.filter(question=cleaned_data['question'], user=owner).count() > 0:
            raise ValidationError('Данный кандидат уже добавлялся ранее')

        if not check_user_status_as_owner(owner):   # Если кандидат не является собственником
            raise ValidationError('Данный кандидат не может быть добавлен')

        return cleaned_data

    def save(self, commit=False):
        candidate = super(AddCandidateForm, self).save(commit)
        candidate.user = get_user_model().objects.get(fullname__icontains=self.cleaned_data['candidate'])
        candidate.save()
        return candidate
