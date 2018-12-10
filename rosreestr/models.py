import json
import re
import xmltodict
from .services import find
from django.db import models
from rosreestr.rosreestrapi import ClientApiRosreestr
from decouple import config


# Create your models here.


# ======================= База запросов на сайте apirosreestr.ru ==========================
class ApiRosreestrRequests(models.Model):
    CHECK_CODE = ((1, 'Создан запрос'),
                  (2, 'Ожидает оплаты'),
                  (3, 'Оплачено, в работе'),
                  (4, 'Выполнено'),
                  (5, 'Ошибка при обработке'),
                  (6, 'Запрос отменен'))
    date_request = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Дата и время запроса')
    cadastre = models.CharField(max_length=50,
                                verbose_name='Кадастровый номер',
                                help_text='Должен соответствовать формату АА:ВВ:CCCCСCC:ККККК')
    objectinfo = models.TextField(null=True, blank=True,
                                  verbose_name='Ответ сервера - ObjectInfoFull')
    invoice = models.IntegerField(null=True, blank=True,
                                  verbose_name='Номер заказа/счета для оплаты')
    payment_allowed = models.BooleanField(default=False, verbose_name='Оплата разрешена')
    sufficient_funds = models.BooleanField(default=False, verbose_name='Достаточно денег для оплаты')
    payment_code = models.CharField(max_length=200, null=True, blank=True,
                                    verbose_name='Код подтверждения оплаты счета')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                verbose_name='Стоимость заказа')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачен')
    document = models.IntegerField(null=True, blank=True,
                                   verbose_name='Номер документа для скачивания')
    status = models.SmallIntegerField(default=1,
                                      choices=CHECK_CODE,
                                      verbose_name='Статус заказа')
    xml_file = models.TextField(null=True, blank=True,
                                verbose_name='Скачанная выписка')
    validated = models.BooleanField(default=False, verbose_name='Подтверждено')

    def get_object_info(self):  # Получет от сервера общую информацию об объекте и сохраняет ее
        if self.objectinfo:
            return True
        clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
        objectinfo = clientapi.post(method='cadaster/objectInfoFull', query=self.cadastre)
        if not clientapi.error:
            self.objectinfo = json.dumps(objectinfo)
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

    def encoded_object(self):  # Возвращает внутренний код объекта
        if self.get_object_info():
            encoded_json = json.loads(self.objectinfo)
            try:
                return encoded_json['encoded_object']
            except:
                return ''
        return ''

    def place_order(self):  # Отправляет заявку на запрос выписки об объекте и получает данные о заказе
        if self.invoice:
            return True
        if self.get_object_info():
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            orderinfo = clientapi.post(method='cadaster/Save_order', documents='XZP',
                                       encoded_object=self.encoded_object())
            if not clientapi.error:
                self.invoice = orderinfo['transaction_id']
                self.status = 1
                self.save()
                return True
            else:
                return False
        return False

    def update_invoice_info(self):  # Получает текущую информацию от состоянии инвойса
        if self.invoice:
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            info = clientapi.post(method='transaction/info', id=self.invoice)
            if not clientapi.error:
                self.payment_code = info['pay_methods']['PA']['confirm_code']  # Сохраним контрольный код оплаты
                self.payment_allowed = info['pay_methods']['PA']['allowed']  # Возможна ли оплата
                self.sufficient_funds = info['pay_methods']['PA']['sufficient_funds']  # Достаточно ли денег на счете
                self.is_paid = info['paid']  # Запишем статус оплаты
                self.save()
                return True
            else:
                return False
        return False

    def update_order_info(self):  # Обновляет текущую информацию о состоянии заказа-ордера
        if self.invoice:
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            orderinfo = clientapi.post(method='cadaster/orders', id=self.invoice)
            if not clientapi.error:
                self.price = orderinfo['documents'][0]['price']
                self.status = orderinfo['documents'][0]['status']
                self.document = orderinfo['documents'][0]['id']
                self.save()
                return True
            else:
                return False
        return False

    def pay_invoice(self):  # Оплачивает инвойс, посылая серверу контрольный код оплаты
        if self.payment_allowed and self.sufficient_funds and self.payment_code:
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            confirmation = clientapi.post(method='transaction/pay', id=self.invoice, confirm=self.payment_code)
            if not clientapi.error:
                self.update_order_info()
                return confirmation['paid']
            else:
                return False
        return False

    def check_owner(self, username):    # Проверяет наличие имени пользователя в списке владельцев в отчете
        if self.xml_file:
            report_dict = xmltodict.parse(self.xml_file)
            try:
                owners = list(find('Person', report_dict['KPOKS']['Realty']))
                for owner in owners:
                    fullname = '{0} {1}'.format(owner['FamilyName'], owner['FirstName']).upper()
                    if fullname == username:
                        self.validated = True
                        self.save()
            except:
                return self.validated
        return self.validated

    def download_file(self):  # Загрузить готовый отчет xml
        if self.status == 4 and self.document and not self.xml_file:
            clientapi = ClientApiRosreestr(token=config('ROSREESTRAPI_KEY'))
            file = clientapi.post(method='cadaster/download', document_id=self.document, format='XML')
            if not clientapi.error:
                self.xml_file = file.replace(re.search('https?://.*Common\.xsl', file)[0], '/static/xsl/Common.xsl')
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
        indexes = [models.Index(fields=['invoice']),]
