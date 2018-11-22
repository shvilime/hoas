import datetime, calendar
from .models import CounterValue, CounterType



# =======================================================================================
# Возвращает период приема показаний для типа счетчика
def list_active_counters():
    return CounterType.objects.filter(active=True)

# =======================================================================================
# Возвращает период приема показаний для типа счетчика
def get_counter_period(type):
    counter = CounterType.objects.get(pk=type.id)
    return counter.start_day, counter.end_day


# =======================================================================================
# Проверяет возможность передачи показаний счетчиков текущей датой
def check_actual_counter_period(type):
    counter = CounterType.objects.get(pk=type.id)
    date = datetime.date.today()
    begin_date = datetime.date(date.year, date.month, max(counter.start_day, 1))
    end_date = datetime.date(date.year, date.month, min(counter.end_day, calendar.monthrange(date.year, date.month)[1]))
    if not ((date >= begin_date) and (date <= end_date)):
        return False
    else:
        return True


# =======================================================================================
# Проверяет показания счетчика на дубли
def check_value_duplication(room, type, date):
    if CounterValue.objects.filter(room=room, type=type, date__month=date.month, date__year=date.year).exists():
        return False
    else:
        return True


# =======================================================================================
# Возвращает предыдущее показание счетчика
def get_previous_value(room, type, date):
    if CounterValue.objects.filter(room=room, type=type, date__lte=date).exists():
        return CounterValue.objects.filter(room=room, type=type, date__lte=date).latest('date').value
    else:
        return 0


# =======================================================================================
# Проверяет показания счетчика на прирост относительно предыдущего значения
def check_value_increment(room, type, date, value):
    previous_value = get_previous_value(room, type, date)
    if previous_value >= value:
        return False
    else:
        return True
