from django.contrib import admin
from .models import Competence, Question

# Register your models here.


class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('number', 'shortname', 'name', 'min_criteria')


admin.site.register(Competence, CompetenceAdmin)
