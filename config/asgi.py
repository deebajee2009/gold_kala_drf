"""
ASGI config for gold_kala_drf project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from apps.asset_trade.routing import websocket_urlpatterns
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')



application = ProtocolTypeRouter({
    # Handles HTTP requests
    "http": get_asgi_application(),

    # Handles WebSocket connections
    "websocket": URLRouter(
        websocket_urlpatterns,
    ),
})
