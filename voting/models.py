from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

# ====================== Тип вопроса согласно жилищного кодекса ========================
class Competence(models.Model):
    TYPE_POLITY = (('OWNERS', 'Собрание собственников'),
                   ('HOAS', 'Собрание участников ТСЖ'))
    TYPE_BASE = ((0, 'Общего числа голосов'),
                 (1, 'Голосов принявших участие'))
    government = models.CharField(max_length=6, choices=TYPE_POLITY,
                                  verbose_name='Орган принятия решения')
    number = models.CharField(max_length=25,
                              verbose_name='Номер статьи Жилищного кодекса')
    shortname = models.CharField(max_length=100,
                                 verbose_name='Краткое содержание статьи Жилищного кодекса')
    name = models.TextField(verbose_name='Полный текст статьи Жилищного кодекса')
    criteria = models.DecimalField(max_digits=8,
                                   decimal_places=5,
                                   default=50,
                                   validators=[MinValueValidator(0.0001), MaxValueValidator(99.9999)],
                                   verbose_name='Критерий принятия решения',
                                   help_text='Решение принято, если ЗА проголосовало более чем указанный % голосов')
    criteria_base = models.SmallIntegerField(default=0, choices=TYPE_BASE,
                                             verbose_name='База для расчета критерия')
    active = models.BooleanField(default=True,
                                 verbose_name='Включено')

    def __str__(self):
        return '{clause}, {description}'.format(clause=self.number, description=self.shortname)

    class Meta:
        ordering = ['number']
        verbose_name = 'Компетенция'
        verbose_name_plural = 'Компетенции'


# ======================= Вопросы поставленные на голосование ==========================
class Question(models.Model):
    TYPE_QUESTION = ((0, 'Обычное голосование'),
                     (1, 'Списочное голосование'))
    competence = models.ForeignKey(Competence,
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name='Тип компетенции общего собрания',
                                   help_text='Компетенция общего собрания ТСЖ в соответствии с жилищным кодексом')
    shortname = models.CharField(max_length=100,
                                 verbose_name='Краткое описание вопроса')
    name = models.TextField(null=True, blank=True,
                            verbose_name='Полное описание вопроса')
    type = models.SmallIntegerField(default=0, choices=TYPE_QUESTION,
                                    verbose_name='Тип голосования')
    date_start = models.DateField(null=True, blank=True,
                                  verbose_name='Дата начала')
    date_end = models.DateField(null=True, blank=True,
                                verbose_name='Дата окончания')

    def __str__(self):
        return '%s' % self.shortname

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
