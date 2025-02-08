from django.core.cache import cache
from django.conf import settings

import redis
from celery import shared_task

from .models import Price
from core import RedisCacheDataBaseManager, PriceFetchService


@shared_task
def fetch_and_update_cache():
    price_data = PriceFetchService.fetch_price()
    data_manager = RedisCacheDataBaseManager()
    tuple_data, list_data = data_manager.prepare_data(price_data)
    data_manager.insert_database(tuple_data)
    data_manager.update_cache(tuple_data)
    data_manger.update_all_cache(list_data)

    # Fetch data from the external API



    # Update the Redis cache with the new data
