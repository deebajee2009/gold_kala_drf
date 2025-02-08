from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from .models import UserWallet

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        return user

class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        moddel = UserWallet
        fields = ['wallet_id', 'user_id', 'balance_toman']
