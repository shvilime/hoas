from django.db.models import Sum
from .models import Owner, Room


# =======================================================================================
# Возвращает общее количество зарегистрированных помещений
def area_total_number():
    return Room.objects.count()


# =======================================================================================
# Возвращает общую площадь зарегистрированных помещений
def area_total_square():
    return Room.objects.aggregate(Sum('square'))


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
# Возвращает сумму долей владельцев из переданного списка
def list_owners_portion(list_owners):
    result = 0
    for owner_id in list_owners:
        result = result + Owner.objects.get(pk=owner_id).portion
    return result


# =======================================================================================
# Возвращает долю предыдущих владельцев в помещении для нового запроса
def previous_owners_portion(owner_request):
    previous_owners = Owner.objects.filter(room=owner_request.room,
                                           date_confirmation__isnull=False,
                                           date_cancellation__isnull=True)
    return list_owners_portion(set(owner.id for owner in previous_owners))


# =======================================================================================
# Анулирует доли предыдущих владельцев в помещении перед подтверждением нового запроса
def cancel_list_owners(list_owners, new_owner):
    for owner_id in list_owners:
        Owner.objects.get(pk=owner_id).cancel(new_owner)
