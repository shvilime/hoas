from django.contrib import admin
from .models import Room, Owner

# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'square', 'cadastre')
    list_filter = ('type',)

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'user', 'date_confirmation')

admin.site.register(Room, RoomAdmin)
admin.site.register(Owner, OwnerAdmin)