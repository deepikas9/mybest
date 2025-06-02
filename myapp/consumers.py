import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from django.utils.timezone import now  # To handle timezones

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
        else:
            # Create a consistent room name
            self.room_name = f"chat_{min(self.user.username, self.other_username)}_{max(self.user.username, self.other_username)}"
            await self.channel_layer.group_add(
                self.room_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message')
        sender = self.scope['user']

        from .models import Message, CustomUser
        receiver = await CustomUser.objects.aget(username=self.other_username)
        message = await Message.objects.acreate(
            sender=sender,
            receiver=receiver,
            content=message_text,
            timestamp=now()
        )

        # Format timestamp as string
        formatted_time = message.timestamp.strftime("%b %d, %H:%M")

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'sender': sender.username,
                'timestamp': formatted_time,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))
