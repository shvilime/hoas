from django.db import models


# Create your models here.

# ======================= ********************************************** ==========================
class CounterType(models.Model):
    name = models.CharField(max_length='100',
                            verbose_name='Тип счетчика')
    class Meta:
        verbose_name = 'Тип счетчика'


# ======================= ********************************************** ==========================
class Counter(models.Model):
    date = models.DateField(verbose_name='Дата показаний')
    type = models.ForeignKey(CounterType, on_delete=models.SET_NULL,
                             verbose_name='Тип счетчика')
    value = models.IntegerField(verbose_name='Показания счетчика')

    class Meta:
        verbose_name = 'Показания'
