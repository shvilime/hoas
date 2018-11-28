import json
from django.db import models
from django.core.validators import RegexValidator
from rosreestr.rosreestrapi import ClientApiRosreestr
from decouple import config


# Create your models here.


# ======================= База запросов на сайте apirosreestr.ru ==========================
class ApiRosreestrRequests(models.Model):
    date_request = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Дата и время запроса')
    cadastre_regex = RegexValidator(regex=r'^\d{2}:\d{2}:\d{6,7}:\d{1,35}$',
                                    message="Должен соответствовать формату АА:ВВ:CCCCСCC:КККККК")
    cadastre = models.CharField(validators=[cadastre_regex], max_length=50,
                                verbose_name='Кадастровый номер',
                                help_text='Должен соответствовать формату АА:ВВ:CCCCСCC:ККККК')
    objectinfo = models.TextField(null=True, blank=True,
                                verbose_name='Ответ сервера - ObjectInfoFull')
    orderinfo = models.TextField(null=True, blank=True,
                                verbose_name='Ответ сервера - Transaction/info')

    def get_object_info(self):     #  Получет от сервера общую информацию об объекте и сохраняет ее
        if self.objectinfo:
            return True
        clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
        objectinfo = clientapi.post(method='Cadaster/objectInfoFull', query=self.cadastre)
        if not clientapi.error:
            self.objectinfo = json.dumps(objectinfo)
            self.save()
            return True
        else:
            return False

    def get_encoded_object(self):    # Возвращает внутренний кодированный код объекта
        if self.get_object_info():
            encoded_json = json.loads(self.objectinfo)
            return encoded_json['encoded_object']
        else:
            return ''

    def document_available(self):    # Возвращает доступность запроса выписки под объекту
        if self.get_object_info():
            encoded_json = json.loads(self.objectinfo)
            return encoded_json['documents']['XZP']['available']

    def place_order(self):
        if self.get_object_info() and not self.order:
            encoded_object = self.get_encoded_object()
            documents = ['XZP']
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            order = clientapi.post(method='Cadaster/Save_order', documents=documents)
            if not clientapi.error:
                self.order = json.dumps(order)
                self.save()
                return True
            else:
                return False
        return False


    def __str__(self):
        return '%s' % self.cadastre

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
