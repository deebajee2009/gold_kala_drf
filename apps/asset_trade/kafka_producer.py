import json

from kafka import KafkaProducer
from decouple import config

class AssetPricePublisher:
    def __init__(self, topic_name):
        self.producer = KafkaProducer(
            bootstrap_servers=f"{config('KAFKA_HOST')}:{config('KAFKA_PORT')}",
            api_version=(0,11,5),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        )
        self.topic_name = topic_name

    def publish_price(self, price_data):
        """Publish new asset price data to Kafka."""
        self.producer.send(self.topic_name, price_data)
        self.producer.flush()

    def close(self):
        """Ensure producer is properly closed."""
        self.producer.flush()  # Ensure any outstanding messages are sent
        self.producer.close()


# Asset price notif publisher
publisher = AssetPricePublisher(topic_name='asset_price_updates')
