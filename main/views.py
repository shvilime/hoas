from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login as authlogin

def home(request):

    return render(request, 'home.html')




# def rooms(request):
#     rooms = Room.objects.all()
#     return render(request, 'rooms.html', {'rooms': rooms, 'typeflat': Room.TYPEFLAT})
#
# def room_owner(request, pk):
#     room = get_object_or_404(Room, pk = pk)
#     return render(request, 'owner.html', {'room': room})

