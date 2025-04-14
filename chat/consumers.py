# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import TourChatMessage
from tour.models import TourBooking
from django.contrib.auth.models import AnonymousUser

class TourChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.tour_id = self.scope['url_route']['kwargs']['tour_id']
        self.room_group_name = f'tour_chat_{self.tour_id}'

        user = self.scope["user"]
        if user == AnonymousUser() or not await self.is_user_registered(user.id, self.tour_id):
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
        user = self.scope["user"]
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        msg = await self.save_message(user.id, self.tour_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg['message'],
                'sender': msg['sender'],
                'timestamp': msg['timestamp'],
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def is_user_registered(self, user_id, tour_id):
        return TourBooking.objects.filter(tour_id=tour_id, user_id=user_id).exists()

    @database_sync_to_async
    def save_message(self, user_id, tour_id, message):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=user_id)
        msg = TourChatMessage.objects.create(
            sender=user,
            tour_id=tour_id,
            message=message
        )
        return {
            'message': msg.message,
            'sender': msg.sender.username,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
