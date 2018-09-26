from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignupForm(UserCreationForm):
    prefix = 'signup'
    email = forms.EmailField(max_length=254,
                             help_text='Обязательное поле. Введите реально существующий адрес')
    first_name = forms.CharField(label='Имя',
                                 max_length=30,
                                 help_text='Ваше имя (как в паспорте)')
    last_name = forms.CharField(max_length=30)
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', max_length=17,
                             help_text='Сотовый номер телефона, для связи')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2', )

class LoginForm(AuthenticationForm):
    prefix = 'login'

