from .models import Owner


# =======================================================================================
# Возвращает историю запросов, посланных пользователем в отношении владения помещениями
def owner_requests_history(user):
    return Owner.objects.filter(user_id=user.pk)

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
