from django.shortcuts import render,redirect
from .models import Room, Message

# Create your views here.
def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']
        
        try:
            existing_room = Room.objects.get(room_name__icontains=room)
        except Room.DoesNotExist:
            r = Room.objects.create(room_name=room)

        return redirect('room', room_name=room, username=username)
    return render(request, 'chat/index.html')

def room(request, room_name, username):
    existing_room = Room.objects.get(room_name__icontains=room_name)
    messages = Message.objects.filter(room=existing_room)
    context = {
        'room_name': room_name,
        'user': username,
        'messages': messages
    }
    return render(request, 'chat/room.html', context)