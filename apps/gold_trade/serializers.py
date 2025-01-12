from rest_framework import serializers
from django.contrib.auth.models import User

from .models import UserBalance, GoldTransaction, GoldPrice
import core

class GoldPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldPrice
        fields = ['price_per_gram', 'date']

class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        fields = ['user_id', 'balance_gold', 'balance_rial', 'date']

class GoldTransactionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = GoldTransaction
        fields = ['transaction_id', 'type', 'gold_weight_gram', 'amount_rial', 'price_per_gram', 'status', 'date']

    def validate(self, data):
        user_balance = UserBalance.objects.filter(user_id=data['user_id']).last()
        
        if data['type'] == GoldTransaction.BUY:
            # Validate if the user has enough money in balance account
            amount_rial = data.get('amount_rial')
            balance_rial = user_balance.balance_rial
            if amount_rial > balance_rial:
                raise serializers.ValidationError("رقم ورودی بیشتر از موجودی حساب می باشد.")
        elif data['type'] == GoldTransaction.SELL:
            # Validate if the user has enough gold in balance account
            gold_weight_gram = data.get('gold_weight_gram')
            balance_gold = user_balance.balance_gold
            
            if gold_weight_gram > balance_gold:
                raise serializers.ValidationError("وزن طلا ورودی بیشتر از طلا در حساب می باشد.")
        
        return data

    def create(self, validated_data):
        # Modify validated_data before saving
        validated_data['status'] = GoldTransaction.COMPLETED
        return super().create(validated_data)
