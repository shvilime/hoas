from django.contrib import admin
from .models import ApiRosreestrRequests


# Register your models here.

class ApiRosreestrRequestsAdmin(admin.ModelAdmin):
    list_display = ('date_request','cadastre')


admin.site.register(ApiRosreestrRequests, ApiRosreestrRequestsAdmin)
