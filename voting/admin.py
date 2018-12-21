from django.contrib import admin
from .models import Competence, Question

# Register your models here.


class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('number', 'shortname', 'criteria', 'criteria_base', 'active')
    list_filter = ('active', 'government')


admin.site.register(Competence, CompetenceAdmin)
