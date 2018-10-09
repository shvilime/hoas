import os
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from PIL import Image


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
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',)


class LoginForm(AuthenticationForm):
    prefix = 'login'


class AvatarUploadForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = get_user_model()
        fields = ('avatar', 'x', 'y', 'width', 'height',)

    def save(self, commit=True):
        user = super(AvatarUploadForm, self).save()
        previous_file = self.initial['avatar'].path
        new_file = user.avatar.path

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(new_file)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((224, 224), Image.ANTIALIAS)
        resized_image.save(new_file)

        if (os.path.exists(previous_file)) and (new_file != previous_file):
            os.remove(previous_file)

        return user
