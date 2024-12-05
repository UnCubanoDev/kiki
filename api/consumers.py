import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Distributor

class DistributorLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "distributors",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "distributors",
            self.channel_name
        )

    async def location_update(self, event):
        await self.send(text_data=json.dumps({
            'distributor_id': event['distributor_id'],
            'lat': event['lat'],
            'lng': event['lng'],
            'name': event['name']
        })) 