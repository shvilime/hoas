from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

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
class MenuItem(MPTTModel):
    menu = models.ForeignKey(Menu,
                             verbose_name='Меню',
                             on_delete=models.CASCADE,
                             related_name='menuitems')
    parent = TreeForeignKey('self',
                            verbose_name='Родительское меню',
                            null=True,
                            blank=True,
                            on_delete=models.CASCADE,
                            related_name='child')
    title = models.CharField(max_length=50,
                             verbose_name='Заголовок')
    url = models.CharField(max_length=100,
                           verbose_name='Cсылка',
                           help_text='Ссылка /faq/ или http://google.com')
    active = models.BooleanField(default=True,
                                 verbose_name='Активность',
                                 help_text='Включить/Выключить пункт меню')
    login_required = models.BooleanField(blank=True,
                                         default=False,
                                         verbose_name='Авторизация',
                                         help_text='Показывать пункт меню только для авторизованных пользователей')

    def __str__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    class MPTTMeta:
        order_insertion_by = ['title']
