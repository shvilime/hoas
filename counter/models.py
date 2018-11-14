from django.db import models


# Create your models here.

# ======================= ********************************************** ==========================
class CounterType(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Тип счетчика')
    measure = models.CharField(max_length=10,
                               verbose_name='Единица измерения')
    active = models.BooleanField(default=True,
                                 verbose_name='Отображать для выбора')

    class Meta:
        verbose_name = 'Тип счетчика'


# ======================= ********************************************** ==========================
class Counter(models.Model):
    date = models.DateField(verbose_name='Дата показаний')
    type = models.ForeignKey(CounterType, on_delete=models.SET_NULL,
                             verbose_name='Тип счетчика')
    value = models.DecimalField(max_digits=8,
                                decimal_places=3,
                                default=0,
                                verbose_name='Показания счетчика')

    class Meta:
        verbose_name = 'Показания'
