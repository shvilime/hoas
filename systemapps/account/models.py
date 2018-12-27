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
    PRIVATE = 0
    ENTITY = 1
    USER_TYPE = (
        (PRIVATE, 'Физическое лицо'),
        (ENTITY, 'Юридическое лицо'),
    )
    username = None
    email = models.EmailField(verbose_name='Email',
                              unique=True, null=False)
    type = models.PositiveSmallIntegerField(choices=USER_TYPE, default=PRIVATE,
                                            verbose_name='Тип пользователя')
    fullname = models.CharField(max_length=100,
                                verbose_name='Наименование',
                                help_text='Фамили, Имя, Отчество (для физ.лиц), Краткое наименование (для юр.лиц)')
    account = models.CharField(verbose_name='Лицевой счет',
                               max_length=20, help_text='Номер лицевого счета')
    phone_regex = RegexValidator(regex=r'^((8|\+7)[\- ]?)(\(?\d{3}\)?[\- ]?)[\d\- ]{7,10}$',
                                 message="Номер должен соответствовать международному формату: '+7(928)1234567'. До 15 цифр")
    phone = models.CharField(verbose_name='Номер телефона',
                             validators=[phone_regex], max_length=17,
                             help_text='Сотовый телефон для связи и подтверждения действий')
    phone_confirmed = models.BooleanField(verbose_name='Телефон подтвержден', default=False)
    date_joined = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    is_member = models.BooleanField(verbose_name='Член ТСЖ', default=False,
                                    help_text='Является членом ТСЖ')
    is_owner = models.BooleanField(verbose_name='Владелец', default=False,
                                   help_text='Является владельцем помещений')
    is_staff = models.BooleanField(verbose_name='Сотрудник', default=False,
                                   help_text='Позволяет сотруднику получить доступ к администрированию сайта')
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    def avatar__path(instance, filename):
        file_name, file_ext = os.path.splitext(filename)
        username = slugify(instance.fullname)
        randomstr = get_random_string(length=10, allowed_chars='abcdefghijklmnopqrstuvwxyz')
        return 'avatars/{user}-[{randomstring}]{ext}'.format(user=username, randomstring=randomstr, ext=file_ext)

    avatar = models.ImageField(verbose_name='Аватар',
                               upload_to=avatar__path,
                               default='avatars/default.jpg',
                               null=True, blank=True)

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return '%s (%s)' % (self.fullname, self.email)

    # def get_full_name(self):
    #     full_name = '%s %s' % (self.lastname, self.firstname)
    #     return full_name.strip()
    #
    # get_full_name.short_description = "Полное имя пользователя"

    def email2user(self, subj, text, from_address=None, **kwargs):
        send_mail(subject=subj,
                  message=text,
                  from_email=from_address,
                  recipient_list=[self.email],
                  **kwargs)
