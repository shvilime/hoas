from django.db import models

# Create your models here.
#<=================================================>
class Menu(models.Model):
    name = models.CharField(max_length=80,
                            verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание',
                                   blank=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

#<=================================================>
class MenuItem(models.Model):
    menu = models.ForeignKey(Menu,
                             verbose_name='Меню',
                             on_delete=models.CASCADE)
    parent = models.ForeignKey('self',
                               verbose_name='Родительское меню',
                               blank=True,
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=150,
                            verbose_name='Наименование')

    login_required = models.BooleanField(blank=True,
                                         default=False,
                                         verbose_name='Авторизация',
                                         help_text='Показывать пункт меню только для авторизованных пользователей')

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
