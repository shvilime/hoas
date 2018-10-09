from django.contrib import admin
from .models import Room

# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    list_display = ('type', 'number', 'square', 'cadastre')


admin.site.register(Room, RoomAdmin)