from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator


# Create your models here.

class Room(models.Model):
    ROOM_TYPE = (('FL', 'Квартира'),
                 ('UN', 'Нежилое помещение'),)

    number = models.CharField(max_length=5,
                              primary_key=True,
                              verbose_name='Номер')
    type = models.CharField(max_length=2,
                            choices=ROOM_TYPE,
                            verbose_name='Тип помещения')
    square = models.DecimalField(max_digits=12,
                                 decimal_places=3,
                                 verbose_name='Площадь')
    cadastre_regex = RegexValidator(regex=r'^\d{2}:\d{2}:\d{6,7}:\d{1,35}$',
                                    message="Должен соответствовать формату АА:ВВ:CCCCСCC:КККККК")
    cadastre = models.CharField(validators=[cadastre_regex], max_length=50,
                                verbose_name='Кадастровый номер',
                                help_text='Должен соответствовать формату АА:ВВ:CCCCСCC:ККККК')

    def __str__(self):
        return '%s %s' % (self.get_type_display(), self.number)

    class Meta:
        ordering = ['number']
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'


class Owner(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
                             verbose_name='Номер помещения')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name='Владелец')
    date_request = models.DateField(auto_now_add=True,
                                    verbose_name='Дата запроса')
    date_confirmation = models.DateField(null=True, blank=True,
                                         verbose_name='Дата подтверждения')

    class Meta:
        unique_together = (('room', 'user', 'date_request'),)
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'
