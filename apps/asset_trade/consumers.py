import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

from .models  import Asset


class AssetPriceSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get user_id from url
        self.user_id = self.scope['url_route']['kwargs'].get('user_id')

        # Query all the assets unique ids from database
        distinct_asset_ids = Asset.objects.values_list('asset_id', flat=True).distinct()
        self.distinct_list = list(distinct_asset_ids)

        # Add user channel layer to the notif group of each asset
        for asset in self.distinct_list:
            await self.channel_layer.group_add(
                f"asset_{asset}",
                self.channel_name
            )
        await self.accept()

    async def disconnect(self, close_code):
        # Close connection and remove user from it
        for asset in self.distinct_list:
            await self.channel_layer.group_discard(
                f"asset_{asset}",
                self.channel_name
            )

    async def receive(self, text_data):
        # Optionally handle incoming messages from WebSocket clients
        pass

    async def send_asset_alarm(self, event):
        asset_id = event['asset_id']
        members_list = cache.get(asset_id)
        if self.user_id in members_list:
            await self.send(text_data=json.dumps(event))
