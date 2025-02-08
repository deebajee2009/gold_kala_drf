from django.contrib.auth.models import User
from django.core.cache import cache
from django.conf import settings

from rest_framework import serializers

from .models import  Asset, AssetTransaction, AssetPrice, AssetlBalance
from apps.accounts.models import UserWallet
import core


class AssetSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = ['name', 'date', 'time', 'price', 'unit']

    def get_date(self, obj):
        recent_price_object = obj.prices.last()
        if recent_price_object:
            return  recent_price.date
        return None

    def get_time(self, obj):
        recent_price_object = obj.prices.last()
        if recent_price_object:
            return  recent_price.time
        return None

    def get_price(self, obj):
        recent_price_object = obj.prices.last()
        if recent_price_object:
            return  recent_price.price
        return None

    def get_unit(self, obj):
        recent_price_object = obj.prices.last()
        if recent_price_object:
            return  recent_price.unit
        return None


class AssetPriceSerializer(serializers.ModelSerializer):
    asset = serializers.StringRelatedField()
    class Meta:
        model = AssetPrice
        fields = ['asset_id', 'date', 'time', 'price', 'unit']




class AssetBalanceSerializer(serializers.ModelSerializer):
    asset_name = serializers.SerializerMethodField()
    class Meta:
        model = AssetlBalance
        fields = ['wallet_id', 'asset_id', 'asset_name','balance_asset', 'date']
    def get_asset_name(self, obj):
        return obj.asset_id.name

class AssetTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetTransaction
        fields = ['user_id','transaction_id', 'type', 'asset_id', 'asset_amount', 'amount_toman', 'status', 'date', 'asset_price']

    def to_representation(self, instance):
        # Get the default representation.
        representation = super().to_representation(instance)
        # Override the price field with a formatted version.
        representation['date'] = instance.date.strftime("%Y/%m/%d %H:%M:%S")
        return representation


    def validate(self, data):
        type = data['type']
        user_id = data.get('user_id')
        if type == AssetTransaction.BUY:
            user_wallet = UserWallet.objects.filter(user_id=user_id).last()

            # Validate if the user has enough money in balance account
            amount_toman = data.get('amount_toman')
            balance_toman = user_wallet.balance_toman
            if amount_toman > balance_toman:
                raise serializers.ValidationError("رقم ورودی بیشتر از موجودی حساب می باشد.")
        elif data['type'] == GoldTransaction.SELL:
            asset_id = data.get('asset_id')
            asset_amount = data.get('asset_amount')
            user_wallet = UserWallet.objects.filter(user_id=user_id).last()
            asset_balance = user_wallet.wallet_balance.filter(asset_id=asset_id).last()

            # Validate if the user has enough asset in balance account
            if asset_balance.balance_asset > asset_amount:
                raise serializers.ValidationError("وزن طلا ورودی بیشتر از طلا در حساب می باشد.")
        return data

    def create(self, validated_data):
        user_id = validated_data['user_id']
        asset_id = validated_data['asset_id']
        asset = Asset.objects.get(asset_id=asset_id)
        cached_data = cache.get(asset.name)

        if validated_data['type'] == AssetTransaction.BUY:
            amount_toman = validated_data['amount_toman']

            if cached_data:
                unit_check = cached_data['unit'] == settings.MONEY_UNIT
                asset_price = cached_data['price']
                if unit_check:
                    asset_amount = round((amount_toman / asset_price), 3)
                else:
                    dollar_price = core.get_dollar_price()
                    asset_price = asset_price * dollar_price
                    asset_amount = round((amount_toman / asset_price), 3)
            else:
                asset_price_object= AssetPrice.objects.filter(asset=asset).last()
                asset_price = asset_price_object.price
                unit_check = asset_price_object.unit == settings.MONEY_UNIT
                if unit_check:
                    asset_amount = round((amount_toman / asset_price), 3)
                else:
                    dollar_price = core.get_dollar_price()
                    asset_price = asset_price * dollar_price
                    asset_amount = round((amount_toman / asset_price), 3)

        elif validated_data['type'] == AssetTransaction.SELL:

            asset_amount = validated_data['amount_toman']
            if cached_data:
                unit_check = cached_data['unit'] == settings.MONEY_UNIT
                asset_price = cached_data['price']
                if unit_check:
                    amount_toman = asset_amount * asset_price
                else:
                    dollar= Asset.objects.get(name=settings.DOLLAR)
                    dollar_price_object = AssetPrice.objects.filter(asset=dollar).last()
                    dollar_price = dollar_price_object.price
                    asset_price = asset_price * dollar_price
                    amount_toman = asset_amount * asset_price
            else:
                asset_price_object= AssetPrice.objects.filter(asset=asset).last()
                asset_price = asset_price_object.price
                unit_check = asset_price_object.unit == settings.MONEY_UNIT
                if unit_check:
                    amount_toman = asset_amount * asset_price
                else:
                    dollar= Asset.objects.get(name=settings.DOLLAR)
                    dollar_price_object = AssetPrice.objects.filter(asset=dollar).last()
                    dollar_price = dollar_price_object.price
                    asset_price = asset_price * dollar_price
                    amount_toman = asset_amount * asset_price

        transaction = AssetTransaction(
            user_id=validated_data['user_id'],
            asset_id=validated_data['asset_id'],
            type=validated_data['type'],
            asset_amount=asset_amount,
            amount_toman=amount_toman,
            status=AssetTransaction.COMPLETED,
            asset_price=asset_price,
            date=core.get_persian_jalali_datetime()
        )
        transaction.save()
        return transaction
