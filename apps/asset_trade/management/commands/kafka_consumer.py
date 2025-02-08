from django.core.management.base import BaseCommand

from apps.asset_trade.kafka_consumer import AssetPriceConsumer

class Command(BaseCommand):
    help = 'Kafka Consumer to consume messages from a Kafka topic'

    def handle(self, *args, **kwargs):
        consumer = AssetPriceConsumer(topic_name='asset_price_updates')
        consumer.listen_for_price_updates()
