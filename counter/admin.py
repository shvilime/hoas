from django.contrib import admin
from .models import CounterType, CounterValue
from datetime import date

# Register your models here.


class CounterTypeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'active',)
    list_filter = ('active',)

#-------- Пользовательский фильтр, чтобы отображать только активные типы счетчиков в админке -----------
class ActiveTypeFilter(admin.SimpleListFilter):
    title = 'Тип счетчика'
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        active_types = CounterType.objects.filter(active=True)
        return [(c.id, c.name) for c in active_types]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type__id__exact=self.value())
        else:
            return queryset

class CounterValueAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'room', 'type', 'value')
    list_filter = (('date', admin.DateFieldListFilter),
                   ActiveTypeFilter,)

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['type'].queryset = CounterType.objects.filter(active=True)
        return super(CounterValueAdmin, self).render_change_form(request, context, *args, **kwargs)

admin.site.register(CounterType, CounterTypeAdmin)
admin.site.register(CounterValue, CounterValueAdmin)