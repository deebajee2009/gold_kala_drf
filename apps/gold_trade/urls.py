from django.urls import path

from .views import BuyGoldView, SellGoldView, UserTransactionHistoryView

urlpatterns = [
    path('transactions/buy/', BuyGoldView.as_view(), name='user-buy-gold'),
    path('transactions/sell/', SellGoldView.as_view(), name='user-sell-gold'),
    path('transactions/user/<int:user_id>/', UserTransactionHistoryView.as_view(), name='user-transaction-history')
]