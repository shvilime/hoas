from decouple import config
from django.shortcuts import render, redirect
from area.rosreestrapi import Client

def home(request):

    apiclient = Client(config('ROSREESTR_KEY'))
    text = apiclient.account(method='info', result='email')

    return render(request, 'home.html')




# def rooms(request):
#     rooms = Room.objects.all()
#     return render(request, 'rooms.html', {'rooms': rooms, 'typeflat': Room.TYPEFLAT})
#
# def room_owner(request, pk):
#     room = get_object_or_404(Room, pk = pk)
#     return render(request, 'owner.html', {'room': room})

