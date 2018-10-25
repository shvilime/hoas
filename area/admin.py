from django.contrib import admin
from django.db.models.functions import Cast
from django.db.models import IntegerField
from .models import Room, Owner


# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'square', 'cadastre')
    list_filter = ('type',)

    def get_queryset(self, request):
        return super(RoomAdmin, self).get_queryset(request).annotate(
            room_integer=Cast('number', IntegerField())).order_by('room_integer')


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'user', 'date_confirmation')


admin.site.register(Room, RoomAdmin)
admin.site.register(Owner, OwnerAdmin)
