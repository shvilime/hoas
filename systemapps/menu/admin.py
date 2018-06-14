from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from systemapps.menu.models import Menu,MenuItem

# Register your models here.

# class MenuItemInline(admin.TabularInline):
#     model = MenuItem
#
# class MenuAdmin(admin.ModelAdmin):
#     inlines = [MenuItemInline,]


admin.site.register(Menu, MPTTModelAdmin)