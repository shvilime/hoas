from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
#<=================================================>
class Menu(models.Model):
    name = models.CharField(max_length=20,
                            verbose_name='Наименование')
    description = models.CharField(max_length=50,
                                   verbose_name='Описание')

    def __str__(self):
        return "%s" % self.description

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

#<=================================================>
class MenuItem(MPTTModel):
    menu = models.ForeignKey(Menu,
                             verbose_name='Меню',
                             on_delete=models.CASCADE)
    parent = TreeForeignKey('self',
                            verbose_name='Родительский пункт',
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
    iconclass = models.CharField(max_length=16,
                                 blank=True,
                                 verbose_name='Класс иконки',
                                 help_text='CSS rласс иконки, оформляющей пункт меню, например icon-facebook'
                                 )
    hrefclass = models.CharField(max_length=15,
                                 blank=True,
                                 verbose_name='Класс ссылки',
                                 help_text='CSS rласс ссылки, обрамляющей URL')
    validators = models.TextField(blank=True,
                                  verbose_name='Видимость меню',
                                  help_text='Функции проверки видимости меню, например ["validators.is_authenticated"]')

    def __str__(self):
        return "%s" % self.title

    class Meta:
        ordering = ['tree_id','lft']
        verbose_name = 'Пункт'
        verbose_name_plural = 'Пункты'

    class MPTTMeta:
        order_insertion_by = ['title']
