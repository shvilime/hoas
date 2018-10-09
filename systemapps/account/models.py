import os
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from uuslug import slugify


# Create your models here.

class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email.lower())
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(verbose_name='Email',
                              unique=True, null=False)
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=30, help_text='Имя (как в паспорте)')
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=30, help_text='Фамилия (как в паспорте)')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Номер должен соответствовать формату: '+999999999'. До 15 цифр")
    phone = models.CharField(verbose_name='Номер телефона',
                             validators=[phone_regex], max_length=17,
                             help_text='Номер должен соответствовать формату:+999999999 до 15 цифр')
    date_joined = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    is_staff = models.BooleanField('Статус сотрудника', default=False,
                                   help_text='Позволяет сотруднику получить доступ к администрированию сайта')
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    def avatar__path(instance, filename):
        file_name, file_ext = os.path.splitext(filename)
        username = slugify(instance.get_full_name())
        randomstr = get_random_string(length=10, allowed_chars='abcdefghijklmnopqrstuvwxyz')
        return 'avatars/{user}-[{randomstring}]{ext}'.format(user=username, randomstring=randomstr, ext=file_ext)

    def avatar__default():
        return '/avatars/default.jpg'

    avatar = models.ImageField(verbose_name='Аватар',
                               upload_to=avatar__path,
                               default=avatar__default,
                               null=True, blank=True)

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return '%s %s (%s)' % (self.last_name, self.first_name, self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def email2user(self, subj, text, from_address=None, **kwargs):
        send_mail(subject=subj,
                  message=text,
                  from_email=from_address,
                  recipient_list=[self.email],
                  **kwargs)
