import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Room

class ChatConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
            self.room_group_name = f'chat_{self.room_name}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
                    
        async def disconnect(self, code):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            await self.close(code)
        
        async def receive(self, text_data):
            print("Received data")
            data_json = json.loads(text_data)
            print(data_json)
            event={
                'type': 'send_message',
                'message': data_json['message'],
                'sender': data_json['sender']
            }
            await self.channel_layer.group_send(
                self.room_group_name,
                event
            )
        async def send_message(self, event):
            data = event["message"]

            await self.create_message(data = data)
            response = {
                'message': data,
                'sender': data["sender"]
            }

            await self.send(text_data=json.dumps(response))
            
        @database_sync_to_async
        def create_message(self, data):
            get_room = Room.objects.get(room_name=data['room_name'])
            if not Message.objects.filter(room=get_room, sender=data['sender'], message=data['message']).exists():
                new_message = Message.objects.create(room=get_room, sender=data['sender'], message=data['message'])
                return new_message
            return None
            