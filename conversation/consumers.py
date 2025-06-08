from channels.generic.websocket import AsyncWebsocketConsumer
import json
from item.models import Item
from .models import Conversation, Message
from channels.db import database_sync_to_async
from django.utils import timezone
from django.db.models import Q

class ChatConsumers(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_number']
        self.path = self.scope['path']
        self.user = self.scope['user']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.send_initial_unread_count()
        await self.mark_messages_as_read()
        await self.channel_layer.group_send(
            f"notify_{self.user.username}",
            {
                "type": "send_notification",
                "data": {
                    "type": "unread_count",
                    "sender": self.user.username,
                    "count": 0,
                }
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def get_or_create_conversation(self, id, text, user):
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

        Message.objects.create(conversation=conversation, text=text, created_by=user)

    @database_sync_to_async
    def mark_messages_as_read(self):
        if 'chat-super' in self.path:
            conversation = Conversation.objects.get(id=self.room_name)
        else:
            item = Item.objects.get(id=self.room_name)
            conversation = Conversation.objects.filter(item=item, number=self.scope["user"]).first()

        if conversation:
            Message.objects.filter(
                conversation=conversation,
                is_read=False
            ).exclude(created_by=self.scope["user"]).update(is_read=True)

    @database_sync_to_async
    def get_other_user_and_unread_count(self):
        # Identify the other user in the conversation and get their unread message count
        if 'chat-super' in self.path:
            conversation = Conversation.objects.get(id=self.room_name)
        else:
            item = Item.objects.get(id=self.room_name)
            conversation = Conversation.objects.filter(item=item, number=self.user).first()

        if not conversation:
            return None, 0

        other_user = [u for u in conversation.number.all() if u != self.user][0]
        count = Message.objects.filter(
            conversation=conversation,
            is_read=False
        ).exclude(created_by=other_user).count()

        return other_user, count

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        user = self.user

        await self.get_or_create_conversation(self.room_name, message, user)

        # Send to chat group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": user.username,
                "timestamp": timezone.now().strftime('%H:%M')
            }
        )

        # 🔔 Notify other user with unread count via NotifyConsumer
        other_user, count = await self.get_other_user_and_unread_count()
        if other_user:
            await self.channel_layer.group_send(
                f"notify_{other_user.username}",
                {
                    "type": "send_notification",
                    "data": {
                        "type": "unread_count",
                        "sender": self.user.username,
                        "count": count,
                    }
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": event['message'],
            "sender": event['sender'],
            "timestamp": event['timestamp']
        }))

    @database_sync_to_async
    def get_total_unread_count(self):
        return Message.objects.filter(
            conversation__number=self.user,
            is_read=False
        ).exclude(created_by=self.user).count()

    async def send_initial_unread_count(self):
        count = await self.get_total_unread_count()
        await self.send(text_data=json.dumps({
            "type": "unread_count",
            "sender": self.user.username,
            "count": count
        }))

class NotifyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return

        self.notify_group_name = f"notify_{self.user.username}"
        await self.channel_layer.group_add(self.notify_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.notify_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        pass  # Optional: Handle ping or command from frontend

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["data"]))
