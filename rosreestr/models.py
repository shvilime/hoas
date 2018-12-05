import json
from django.db import models
from django.core.validators import RegexValidator
from rosreestr.rosreestrapi import ClientApiRosreestr
from decouple import config


# Create your models here.


# ======================= База запросов на сайте apirosreestr.ru ==========================
class ApiRosreestrRequests(models.Model):
    STATUS_CODE = ((1, 'Создан'),
                   (2, 'Объект идентифицирован'),
                   (3, 'Отправлен заказ'),
                   (4, 'Выставлен инвойс'),
                   (5, 'Оплачен'))
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
    status = models.SmallIntegerField(default=1,
                                      choices=STATUS_CODE,
                                      verbose_name='Статус заказа')

    def get_object_info(self):  # Получет от сервера общую информацию об объекте и сохраняет ее
        if self.objectinfo:
            return True
        clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
        objectinfo = clientapi.post(method='cadaster/objectInfoFull', query=self.cadastre)
        if not clientapi.error:
            self.objectinfo = json.dumps(objectinfo)
            self.status = 2
            self.save()
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

    def place_order(self):  # Отправляет заявку на запрос выписки об объекте и получает данные о заказе
        if self.orderinfo:
            return True
        if self.get_object_info():
            encoded_object = json.loads(self.objectinfo)['encoded_object']
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            orderinfo = clientapi.post(method='cadaster/Save_order', documents='XZP', encoded_object=encoded_object)
            if not clientapi.error:
                self.orderinfo = json.dumps(orderinfo)
                self.status = 3
                self.save()
                return True
            else:
                return False
        return False

    def get_invoice(self):  # Получает от сервера информацию об инвойсе для оплаты ранее отосланного заказа
        if self.place_order():
            invoice = json.loads(self.orderinfo)['transaction_id']
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            transaction = clientapi.post(method='transaction/info', id=invoice)
            if not clientapi.error:
                self.transactioninfo = json.dumps(transaction)
                if not transaction['paid']:
                    self.status = 4
                self.save()
                return True
            else:
                return False
        return False

    def invoice_id(self):  # Возвращает уникальный номер инвойса
        if self.transactioninfo:
            try:
                return json.loads(self.transactioninfo)['id']
            except:
                return ''
        return ''

    def get_confirm_code(self):  # Проверяет возможность оплаты инвойса и возвращает контрольный код оплаты
        if self.transactioninfo:
            encoded_json = json.loads(self.transactioninfo)
            try:
                payment_allowed = encoded_json['pay_methods']['PA']['allowed']  # Возможна ли оплата
                money_enough = encoded_json['pay_methods']['PA']['sufficient_funds']  # Достаточно ли денег на счете
                payment_code = encoded_json['pay_methods']['PA']['confirm_code']  # Какой контрольный код оплаты
            except:
                return ''
            if payment_allowed and money_enough:
                return payment_code
        return ''

    def invoice_is_paid(self):  # Проверяет был ли оплачен ранее
        if self.transactioninfo:
            try:
                return json.loads(self.transactioninfo)['paid']  # Статус оплаты
            except:
                return False
        return False

    def pay_invoice(self):  # Оплачивает инвойс, посылая серверу контрольный код оплаты
        payment_code = self.get_confirm_code()
        if payment_code:
            invoice = json.loads(self.orderinfo)['transaction_id']
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            confirmation = clientapi.post(method='transaction/pay', id=invoice, confirm=payment_code)
            if not clientapi.error:
                self.status = 5
                self.save()
                return confirmation['paid']
            else:
                return False
        return False

    def order_info(self):
        invoice = self.invoice_id()
        if invoice:
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            orderinfo = clientapi.post(method='cadaster/orders', id=invoice)
            if not clientapi.error:
                return True
            else:
                return False
        return False

    def __str__(self):
        return '%s' % self.cadastre

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
