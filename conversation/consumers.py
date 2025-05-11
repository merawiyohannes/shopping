from channels.generic.websocket import AsyncWebsocketConsumer
import json
from item.models import Item
from .models import Conversation, Message
from channels.db import database_sync_to_async
from django.utils import timezone

def notification():
    print("ws is running ")


class ChatConsumers(AsyncWebsocketConsumer):
            
    async def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['room_number']
        self.path = self.scope['path']
        self.user = self.scope['user']
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
    
    @database_sync_to_async
    def get_create_conversation(self, id, text, user):
        if 'chat-super' in self.path:
            conversation = Conversation.objects.get(id=id)
        else:
            item = Item.objects.get(id=self.room_name)
            conversation = Conversation.objects.filter(item=item, number=user).first()
            if not conversation:
                conversation = Conversation.objects.create(item=item)
                conversation.number.add(self.user)
                conversation.number.add(item.created_by)
                conversation.save()
        msg = Message.objects.create(conversation=conversation, text=text, created_by=user)

    
    async def receive(self, text_data=None, bytes_data=None):
        
        text_data = json.loads(text_data)
        message = text_data["message"]
        user = self.scope['user']
        await self.get_create_conversation(self.room_name, message, user)
        
        await self.channel_layer.group_send(self.room_group_name, {
            "type": "chat_message",
            "message": message,
            "sender": user.username,
            "timestamp": timezone.now().strftime('%H:%M')
        })
        
        
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']
        await self.send(text_data=json.dumps(
            {
                "message": message,
                "sender": sender,
                "timestamp": timestamp
            }
        ))