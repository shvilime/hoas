from django.contrib import admin
from .models import ApiRosreestrRequests


# Register your models here.

class ApiRosreestrRequestsAdmin(admin.ModelAdmin):
    readonly_fields = ('cadastre','objectinfo','is_paid','payment_code','validated',
                       'sufficient_funds','payment_allowed','price','status','document','xml_file')
    list_display = ('date_request','cadastre','price','status')


admin.site.register(ApiRosreestrRequests, ApiRosreestrRequestsAdmin)
