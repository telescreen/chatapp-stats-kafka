import json
import logging
from datetime import datetime
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from confluent_kafka import Producer


logger = logging.getLogger(__name__)
kafka_producer = Producer(settings.KAFKA)
CHAT_USERS_TOPIC = 'chat_users'

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = "chat_{}".format(self.room_name)

        # Join room group
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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        logger.info("Received from client: {}".format(text_data_json))
        kafka_producer.produce(CHAT_USERS_TOPIC,
            key=username,
            value=json.dumps({
                'username': username,
                'message_time': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                'message_content': message
            }))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data = json.dumps({
            'message': message,
            'username': username
        }))