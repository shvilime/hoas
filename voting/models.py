from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from area.models import Owner


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


# ======================= Кандидаты, при голосовании по вопросам списочного типа ==========================
class Candidate(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='questions',
                                 verbose_name='Вопрос на голосование')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='candidates',
                             verbose_name='Кандидат')
    nominator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                  related_name='nominators',
                                  verbose_name='Кем номинирован')
    date_nominate = models.DateField(auto_now_add=True,
                                     verbose_name='Дата выдвижения')
    date_cancellation = models.DateField(null=True, blank=True,
                                         verbose_name='Дата отказа от участия')

    def __str__(self):
        return '%s' % self.user

    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'


# ============================== Голоса, отданные по вопросам голосования =================================
class Vote(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 verbose_name='Вопрос на голосование')
    candidate = models.ForeignKey(Candidate, null=True, blank=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name='Кандидат')
    owner = models.ForeignKey(Owner,
                              on_delete=models.CASCADE,
                              verbose_name='Владелец')
    date_voting = models.DateField(auto_now_add=True,
                                   verbose_name='Дата голосования')

    def __str__(self):
        return '{question} - {date} - {user}'.format(date=self.date_voting,
                                                     question=self.question,
                                                     user=self.owner.user)

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
