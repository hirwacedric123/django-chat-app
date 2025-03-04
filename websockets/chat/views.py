from django.shortcuts import render,redirect
from .models import Room, Message

# Create your views here.
def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        room_name = request.POST['room']
        
        try:
            existing_room = Room.objects.get(room_name=room)
            if not username or not room_name:
                return render(request, 'chat/index.html', {'error': 'Username and room name are required.'})
        except Room.DoesNotExist:
            Room.objects.create(room_name=room)

        return redirect('room', room_name=room_name, username=username)
    return render(request, 'chat/index.html')

def room(request, room_name, username):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': username
    })