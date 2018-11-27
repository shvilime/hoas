from django.db import models
from django.core.validators import RegexValidator
from .rosreestrapi import *
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
    order = models.TextField(null=True, blank=True,
                                verbose_name='Ответ сервера - Save_order')

    def get_object_info(self):
        if self.objectinfo_response:
            return True
        clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
        objectinfo = clientapi.post(method='Cadaster/objectInfoFull', query=self.cadastre)
        if not clientapi.error:
            self.objectinfo_response = json.dumps(objectinfo)
            self.save()
            return True
        else:
            return False

    def get_encoded_object(self):
        if self.get_object_info():
            encoded_json = json.loads(self.objectinfo)
            return encoded_json['encoded_object']
        else:
            return ''

    def document_available(self):
        if self.get_object_info():
            encoded_json = json.loads(self.objectinfo)
            return encoded_json['documents']['XZP']['available']

    def place_order(self):
        if self.get_object_info():
            encoded_object = self.get_encoded_object()
            documents = ['XZP']

        return


    def __str__(self):
        return '%s' % self.cadastre

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
