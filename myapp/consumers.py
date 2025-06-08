import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print('connection to room : ', self.room_group_name)

        # Optional: Validate user in room before accept
        if not await self.is_user_in_room():
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_username = data.get('sender')
        receiver_username = data.get('receiver')

        if not message or not sender_username or not receiver_username:
            # You may want to handle errors or invalid data here
            return

        await self.save_message(sender_username, receiver_username, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
                'receiver': receiver_username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'receiver': event['receiver'],
        }))

    @database_sync_to_async
    def save_message(self, sender_username, receiver_username, message):
        try:
            sender = User.objects.get(username=sender_username)
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            # If either user doesn't exist, skip saving
            return
        ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)

    @database_sync_to_async
    def is_user_in_room(self) -> bool:
        """
        Simple check: The room name is expected to be 'user1_user2'.
        We check if current user is either user1 or user2.
        """
        current_user = self.scope['user']
        users_in_room = self.room_name.split('_')
        return current_user.username in users_in_room




# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
# from .models import ChatMessage

# User = get_user_model()

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # room_name can be a combined string like 'user1_user2'
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
#         sender_username = data['sender']
#         receiver_username = data['receiver']  # You need to send this from frontend

#         # Save message to DB asynchronously
#         await self.save_message(sender_username, receiver_username, message)

#         # Broadcast message to the group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': sender_username,
#                 'receiver': receiver_username,
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender': event['sender'],
#             'receiver': event['receiver'],
#         }))

#     @database_sync_to_async
#     def save_message(self, sender_username, receiver_username, message):
#         try:
#             sender = User.objects.get(username=sender_username)
#             receiver = User.objects.get(username=receiver_username)
#         except User.DoesNotExist:
#             # If either user doesn't exist, skip saving
#             return
#         ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)
