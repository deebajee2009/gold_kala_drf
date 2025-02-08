from django.urls import re_path
from .consumers import AssetPriceSocketConsumer

websocket_urlpatterns = [
    re_path(r'ws/gold-price/<int:user_id>/', AssetPriceSocketConsumer.as_asgi()),
]
