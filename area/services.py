from django.db.models import Sum
from .models import Owner, Room


# =======================================================================================
# Возвращает общее количество зарегистрированных помещений
def area_total_number():
    return Room.objects.count()


# =======================================================================================
# Возвращает общую площадь зарегистрированных помещений
def area_total_square():
    return Room.objects.aggregate(Sum('square'))['square__sum']


# =======================================================================================
# Возвращает общее количество активных собственников
def owner_total_number():
    return Owner.objects.filter(date_confirmation__isnull=False, date_cancellation__isnull=True).count()


# =======================================================================================
# Возвращает общее количество активных собственников
def owner_total_square():
    return Owner.objects.filter(date_confirmation__isnull=False,
                                date_cancellation__isnull=True).aggregate(Sum('room__square'))['room__square__sum']


# =======================================================================================
# Возвращает историю запросов, посланных пользователем в отношении владения помещениями
# all - все запросы, active - только активные
def owner_requests_history(user, **options):
    if options.get('active'):
        result = Owner.objects.filter(user_id=user.pk, date_confirmation__isnull=False,
                                      date_cancellation__isnull=True)
    else:
        result = Owner.objects.filter(user_id=user.pk)
    return result


# =======================================================================================
# Возвращает сумму долей владельцев из переданного queryset
def sum_owners_portion(queryset_owners):
    return queryset_owners.aggregate(summa=Sum('portion'))['summa'] or 0


# =======================================================================================
# Возвращает долю предыдущих владельцев в помещении для нового запроса
def sum_previous_owners_portion(new_owner):
    previous_owners = Owner.objects.filter(room=new_owner.room,
                                           date_confirmation__isnull=False,
                                           date_cancellation__isnull=True)
    return sum_owners_portion(previous_owners)


# =======================================================================================
# Проверяет статус пользователя как владельца и обновляет его
def check_user_status_as_owner(user):
    user.is_owner = owner_requests_history(user, active=True).exists()    # Есть ли активные записи о собственности
    user.save()
    return user.is_owner


# =======================================================================================
# Анулирует доли предыдущих владельцев в помещении перед подтверждением нового запроса
def cancel_list_owners(queryset_owners, new_owner):
    for owner in queryset_owners:      # Для каждого предыдущего владельца в списке
        owner.cancel(new_owner)        # Анулируем запись о владении
        check_user_status_as_owner(owner.user)    # Проверим и обновим статус пользователя как владельца
