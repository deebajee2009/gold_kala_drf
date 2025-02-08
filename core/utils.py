import requests
from datetime import time, datetime

import redis
from django.core.cache import cache
from decouple import config


class PriceFetchService:
    # Api for gold, currencies, cryptocurrencies proces in Toman from http://brsapi.ir
    PRICE_API_URL = 'https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency.json'

    @staticmethod
    def fetch_price():
        response = requests.get(PriceFetchService.PRICE_API_URL)
        data = response.json()
        data["asset"] = data.pop("name") # Change key name of name to asset
        return data

class RedisCacheDataBaseManager:
    def __init__(self):
        # Create a Redis client
        self.redis_client = redis.StrictRedis(
            host=config('REDIS_HOST'), port=config('REDIS_PORT'), db=1, decode_responses=True
        )

    def insert_database(self, data):
        from apps.gold_trade.models import Asset, AssetPrice

        for asset_name, asset_object in data:
            asset = Asset.objects.get(name=asset_name)
            price = int(asset_object['price'])
            time_string = asset_object['time']
            date_string = asset_object['date']
            hour, minute = map(int, time_string.split(':'))
            year, month, day = map(int, date_string.split('/'))
            time_object = time(hour=hour, minute=minute)
            date_object = jdatetime.date(year, month, day)
            AssetPrice.objects.Create(asset=asset, date=date_object, time=time_object, price=price)

    def set_cache(self, key, value):
        """Set a key-value pair in Redis cache."""
        self.redis_client.set(key, value)

    def get_cache(self, key):
        """Get a value from Redis cache by key."""
        return self.redis_client.get(key)

    def update_cache(self, data):
        for asset_name, asset_object in data:
            self.set_cache(asset_name, asset_object)
    def update_all_cache(self, data):
        self.set_cache('all_data', data)
    def prepare_data(self, data_dict):
        """Update multiple keys in Redis cache based on the fetched data."""

        gold = data_dict['gold'][2]['name'] # Get Farsi name of Asset
        gold_object = data_dict['gold'][2] # Get Object of asset from api response like data, time & price

        dollar = data_dict['currency'][0]['name']
        dollar_object = data_dict['currency'][0]

        bitcoin = data_dict['cryptocurrency'][0]['name']
        bitcoin_object = data_dict['cryptocurrency'][0]

        ethereum = data_dict['cryptocurrency'][1]['name']
        ethereum_object = data_dict['cryptocurrency'][1]
        tuple_list = [
            (gold, gold_object),
            (dollar, dollar_object),
            (bitcoin, bitcoin_object),
            (ethereum, ethereum_object)
        ]

        all_list = [
            gold_object,
            dollar_object,
            bitcoin_object,
            ethereum_object
        ]

        return tuple_list, all_list

def get_dollar_price():
    from apps.gold_trade.serializers import AssetSerializer

    dollar_string = 'دلار'
    dollar_cache_price = cache.get(dollar_string)
    if dollar_cache_price:
        return dollar_cache_price.price

    dollar= Asset.objects.get(name=dollar_string)
    dollar_price_object = AssetPrice.objects.filter(asset=dollar).last()
    dollar_price = dollar_price_object.price
    serializer = AssetSerializer(dollar)
    cache.set(dollar_string, serializer.data)
    return dollar_price

def get_persian_jalali_datetime():
    import jdatetime


    # Create a datetime object (Gregorian)
    gregorian_datetime = datetime.now()

    # Convert to Jalali datetime
    jalali_datetime = jdatetime.datetime.fromgregorian(datetime=gregorian_datetime)
    return jalali_datetime
