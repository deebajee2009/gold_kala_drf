# admin.py
from django.contrib import admin
from .models import GoldPrice, UserBalance, GoldTransaction

# Register the Transaction model
admin.site.register(GoldPrice)
admin.site.register(UserBalance)
admin.site.register(GoldTransaction)