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
        
        async def receive(self, data_received):
            data_json = json.loads(data_received)
            message = data_json['message']
            username = data_json['username']
            room = await self.get_room()
            await self.save_message(room, username, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username
                }
            )
            
           




