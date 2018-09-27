from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignupForm(UserCreationForm):
    prefix = 'signup'
    email = forms.EmailField(max_length=254,
                             help_text='Обязательное поле. Введите реально существующий адрес')
    first_name = forms.CharField(label='Имя',
                                 max_length=30,
                                 help_text='Ваше имя (как в паспорте)')
    last_name = forms.CharField(label='Фамилия',
                                max_length=30,
                                help_text='Ваша фамилия (как в паспорте)')
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', )

class LoginForm(AuthenticationForm):
    prefix = 'login'

