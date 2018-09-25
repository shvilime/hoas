from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignupForm(UserCreationForm):
    prefix = 'signup'
    username = forms.CharField(label='Логин пользователя',
                               max_length=20)
    first_name = forms.CharField(label='Имя',
                                 max_length=30,
                                 help_text='Ваше имя (как в паспорте)')
    last_name = forms.CharField(label='Фамилия',
                                max_length=30,
                                help_text='Ваша фамилия (как в паспорте)')
    email = forms.EmailField(max_length=254,
                             help_text='Обязательное поле. Введите реально существующий адрес')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class LoginForm(AuthenticationForm):
    prefix = 'login'
    # username = forms.CharField(label='Логин пользователя',
    #                            max_length=20)
