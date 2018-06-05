from django.db import models

# Create your models here.

class SocialNetworkLinks(models.Model):
    name = models.CharField(max_length=30,
                            verbose_name='Название сети')
    link = models.CharField(max_length=80,
                            verbose_name='Ссылка')
    iconclass = models.CharField(max_length=16,
                                 verbose_name='Класс иконки')
    hrefclass = models.CharField(max_length=15,
                                 verbose_name='Класс ссылки')
    order = models.SmallIntegerField(null=False, default=0,
                                     verbose_name='Порядковый номер')
    enabled = models.BooleanField(verbose_name='Включено')

    def __str__(self):
        return 'Соцсеть %s. Включено: %s' % (self.name, self.enabled)

    class Meta:
        ordering = ['order']
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'