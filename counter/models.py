from django.db import models
from django.utils import formats
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from area.models import Room


# Create your models here.

# ======================= ********************************************** ==========================
class CounterType(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Тип счетчика')
    measure = models.CharField(max_length=10,
                               verbose_name='Единица измерения')
    start_day = models.IntegerField(verbose_name='Дата начала',
                                    default=1,
                                    validators=[MinValueValidator(1), MaxValueValidator(31)],
                                    help_text='Дата месяца, с которого разрешено вводить показания')
    end_day = models.IntegerField(verbose_name='Дата окончания',
                                  default=31,
                                  validators=[MinValueValidator(1), MaxValueValidator(31)],
                                  help_text='Дата месяца, до которой разрешено вводить показания')
    active = models.BooleanField(default=True,
                                 verbose_name='Отображать для выбора')

    def __str__(self):
        return '{name} ({measure})'.format(name=self.name,
                                           measure=self.measure)

    class Meta:
        verbose_name = 'Тип счетчика'
        verbose_name_plural = 'Типы счетчиков'


# ======================= ********************************************** ==========================
class CounterValue(models.Model):
    date = models.DateField(verbose_name='Дата показаний')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name='Владелец')
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
                             verbose_name='Номер помещения')
    type = models.ForeignKey(CounterType, on_delete=models.SET_NULL,
                             null=True,
                             verbose_name='Тип счетчика')
    value = models.DecimalField(max_digits=8,
                                decimal_places=3,
                                default=0,
                                verbose_name='Показания счетчика')

    def __str__(self):
        return '{date},{user},{type},{value}'.format(date=formats.date_format(self.date),
                                                     type=self.type,
                                                     user=self.user.get_full_name(),
                                                     value=self.value)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Показания'
        verbose_name_plural = 'Показания'
