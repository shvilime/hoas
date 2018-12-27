import os, re
from django.conf import settings
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from PIL import Image


class SignupForm(UserCreationForm):
    prefix = 'signup'
    email = forms.EmailField(max_length=254,
                             help_text='Обязательное поле. Введите реально существующий адрес')
    class Meta:
        model = get_user_model()
        fields = ('email', 'type', 'fullname', 'password1', 'password2',)


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
        new_file = user.avatar.path
        previous_file = ''
        if (settings.MEDIA_URL + self.initial['avatar'].field.default != self.initial['avatar'].url):
            previous_file = self.initial['avatar'].path

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


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['phone']

    def clean(self):
        self.cleaned_data = super(EmailChangeForm, self).clean()
        self.cleaned_data['phone'] = re.sub('[- \(\)]', '', self.cleaned_data.get('phone'))
