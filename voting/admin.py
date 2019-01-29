from django.contrib import admin
from .models import Competence, Question, Candidate

# Register your models here.


class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('number', 'shortname', 'criteria', 'criteria_base', 'active')
    list_filter = ('active', 'government')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('type', 'competence', 'shortname', 'date_start', 'date_end')
    list_filter = ('date_start',)

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['competence'].queryset = Competence.objects.filter(active=True)
        return super(QuestionAdmin, self).render_change_form(request, context, *args, **kwargs)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('question', 'user')


admin.site.register(Competence, CompetenceAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Candidate, CandidateAdmin)
