from django.urls import path

from .views import BuyAssetView, SellAssetView, TransactionHistoryView, PriceView

urlpatterns = [
    path('transactions/buy/', BuyAssetView.as_view(), name='buy-asset'),
    path('transactions/sell/', SellAssetView.as_view(), name='sell-asset'),
    path('transactions/user/<int:user_id>/', TransactionHistoryView.as_view(), name='transactions-history'),
    path('prices/', PriceView.as_view(), name='asset-price')
]
