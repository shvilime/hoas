from django.contrib import admin
from .models import Room, Owner

# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    list_display = ('type', 'number', 'square', 'cadastre')

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'date_confirmation')

admin.site.register(Room, RoomAdmin)
admin.site.register(Owner, OwnerAdmin)