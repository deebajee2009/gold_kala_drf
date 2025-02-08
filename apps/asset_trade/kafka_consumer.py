import json

from kafka import KafkaConsumer
from decouple import config
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class AssetPriceConsumer:
    def __init__(self, topic_name):
        self.consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=f"{config('KAFKA_HOST')}:{config('KAFKA_PORT')}",
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='asset_price_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def listen_for_price_updates(self):
        """Consume asset price updates from Kafka and handle notifications."""
        for message in self.consumer:

            self.send_push_notification_to_users(message)

    def send_push_notification_to_users(self, message):
        price = message.price
        asset_id = message.asset_id
        unit = message.unit

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"asset_{asset_id}",  # The group name where WebSocket users are listening
            {
                "type": "send_asset_alarm",
                "price": price,
                "asset_id": asset_id,
                "unit": unit
            }
        )
