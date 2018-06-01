from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login as authlogin

def home(request):

    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)

        if user is not None:
            # correct username and password login the user
            authlogin(request, user)
            return redirect('home')

    return render(request, 'home.html', {'user': user })




# def rooms(request):
#     rooms = Room.objects.all()
#     return render(request, 'rooms.html', {'rooms': rooms, 'typeflat': Room.TYPEFLAT})
#
# def room_owner(request, pk):
#     room = get_object_or_404(Room, pk = pk)
#     return render(request, 'owner.html', {'room': room})

