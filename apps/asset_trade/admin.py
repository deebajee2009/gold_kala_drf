# admin.py
from django.contrib import admin
from .models import *

# Register the Asset_trade models
admin.site.register(Asset)
admin.site.register(AssetPrice)
admin.site.register(AssetlBalance)
admin.site.register(AssetTransaction)
admin.site.register(AssetUsersAlaram)
