from django.contrib import admin
from .models import ApiRosreestrRequests


# Register your models here.

class ApiRosreestrRequestsAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(ApiRosreestrRequests, ApiRosreestrRequestsAdmin)
