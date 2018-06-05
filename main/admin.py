from django.contrib import admin

# Register your models here.

from main.models import SocialNetworkLinks

class SocialNetworkLinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'enabled')

admin.site.register(SocialNetworkLinks, SocialNetworkLinksAdmin)