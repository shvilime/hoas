from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from systemapps.menu.models import Menu, MenuItem

# Register your models here.

class MenuAdmin(admin.ModelAdmin):
    exclude = ['parent']
#    def get_model_perms(self, request):     #hide this Model in Admin
#        return {}

class MenuItemAdmin(DraggableMPTTAdmin):
    list_filter = ('menu',)
    expand_tree_by_default = True
    list_display = ('tree_actions', 'indented_title','url','active')
    list_display_links = ('indented_title',)

admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)