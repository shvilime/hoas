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

    def document_available(self):  # Возвращает доступность запроса выписки под объекту
        if self.get_object_info():
            encoded_json = json.loads(self.objectinfo)
            try:
                return encoded_json['documents']['XZP']['available']
            except:
                return False
        return False

    def place_order(self):
        if self.orderinfo:
            return True
        if self.get_object_info():
            encoded_object = json.loads(self.objectinfo)['encoded_object']
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            orderinfo = clientapi.post(method='cadaster/Save_order', documents='XZP', encoded_object=encoded_object)
            if not clientapi.error:
                self.orderinfo = json.dumps(orderinfo)
                return True
            else:
                return False
        return False

    def get_invoice(self):
        if self.transactioninfo:
            return True
        if self.place_order():
            invoice = json.loads(self.orderinfo)['transaction_id']
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            transaction = clientapi.post(method='transaction/info', id=invoice)
            if not clientapi.error:
                self.transactioninfo = json.dumps(transaction)
                return True
            else:
                return False
        return False

    def get_confirm_code(self):
        if self.get_invoice():
            encoded_json = json.loads(self.transactioninfo)
            try:
                payment_allowed = encoded_json['pay_methods']['PA']['allowed']
                money_enough = encoded_json['pay_methods']['PA']['sufficient_funds']
                payment_code = encoded_json['pay_methods']['PA']['confirm_code']
            except:
                return ''
            if payment_allowed and money_enough:
                return payment_code
        return ''

    def pay_invoice(self):
        payment_code =  self.get_confirm_code()
        if payment_code:
            invoice = json.loads(self.orderinfo)['transaction_id']
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            confirmation = clientapi.post(method='transaction/pay', id=invoice, confirm=payment_code)
            return confirmation['paid']
        return False

    def __str__(self):
        return '%s' % self.cadastre

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
