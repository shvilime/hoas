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
                                 verbose_name='Ответ сервера - Save_order')
    transactioninfo = models.TextField(null=True, blank=True,
                                       verbose_name='Ответ сервера - Transaction/info')

    def get_object_info(self):  # Получет от сервера общую информацию об объекте и сохраняет ее
        if self.objectinfo:
            return True
        clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
        objectinfo = clientapi.post(method='cadaster/objectInfoFull', query=self.cadastre)
        if not clientapi.error:
            self.objectinfo = json.dumps(objectinfo)
            return True
        else:
            return False

    def get_encoded_object(self):  # Возвращает внутренний кодированный код объекта
        if self.get_object_info():
            encoded_json = json.loads(self.objectinfo)
            return encoded_json['encoded_object']
        else:
            return ''

    def document_available(self):  # Возвращает доступность запроса выписки под объекту
        if self.get_object_info():
            encoded_json = json.loads(self.objectinfo)
            return encoded_json['documents']['XZP']['available']

    def place_order(self):
        if self.orderinfo:
            return True
        if self.get_object_info():
            encoded_object = self.get_encoded_object()
            documents = 'XZP'
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            orderinfo = clientapi.post(method='cadaster/Save_order', documents=documents, encoded_object=encoded_object)
            if not clientapi.error:
                self.orderinfo = json.dumps(orderinfo)
                return True
            else:
                return False
        return False

    def get_invoice_number(self):
        if self.place_order():
            encoded_json = json.loads(self.orderinfo)
            return encoded_json['transaction_id']
        else:
            return ''

    def get_invoice(self):
        if self.orderinfo:
            invoice = self.get_invoice_number()
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            transaction = clientapi.post(method='transaction/info', id=invoice)
            if not clientapi.error:
                self.transactioninfo = json.dumps(transaction)
                return True
            else:
                return False
        return False


    def __str__(self):
        return '%s' % self.cadastre

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
