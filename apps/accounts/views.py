from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import action

from .serializers import UserSerializer, LoginSerializer, UserWalletSerializer
from .models import UserWallet
from apps.asset_trade.serializers import AssetBalanceSerializer
from apps.asset_trade.models import AssetlBalance, AssetUsersAlaram

User = get_user_model()

# Signup view
class SignupView(generics.CreateAPIView):
    """
    View for handling user signup
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# Login view
class LoginView(generics.GenericAPIView):
    """
    View for handling login and authentication
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

# Logout view
class LogoutView(generics.GenericAPIView):
    """
    View for handling logout of user
    """
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# Refresh token view
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class UserWalletAssetViewSet(viewsets.ViewSet):
    """
    A ViewSet that handles two URLs:
    1. /user/<int:user_id>/wallet -> Returns the wallet information of the user
    2. /user/<int:user_id>/assets -> Returns the assets bought by the user
    3. /user/<int:user_id>/asset-member -> Add or remove user from asset price notif group
    """
    lookup_field = 'user_id'

    @action(detail=True, methods=['get'], url_path='wallet')
    def wallet(self, request, user_id=None):
        user = get_object_or_404(User, user_id=user_id)
        wallet = get_object_or_404(UserWallet, user_id=user)

        # Serialize the wallet data
        serializer = UserWalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='assets')
    def assets(self, request, user_id=None):
        # Get the user and their purchased assets
        user = get_object_or_404(User, user_id=user_id)
        wallet = get_object_or_404(UserWallet, user_id=user_id)
        assets = AssetlBalance.objects.filter(wallet_id=wallet)

        # Serialize the assets data
        serializer = AssetBalanceSerializer(assets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='asset-member')
    def asset_member(self, request, user_id=None):
        """
        Add a user to the asset's members group based on asset_id provided in the request body.
        """
        user = get_object_or_404(User, user_id=user_id)
        asset_id = request.data.get('asset_id')
        if not asset_id:
            return Response({'error': 'asset_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the asset based on asset_id
        asset = get_object_or_404(AssetUsersAlaram, asset_id=asset_id)

        # Add the asset to the user's following group (many-to-many relation)
        asset.members.add(user)

        return Response({'message': f'User {user.username} added to following group.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='asset-member')
    def asset_member(self, request, user_id=None):
        """
        Remove a user from the assets's members group based on asset_id provided in the request body.
        """
        user = get_object_or_404(User, user_id=user_id)

        # Get asset_id from the request data
        asset_id = request.data.get('asset_id')
        if not asset_id:
            return Response({'error': 'asset_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the asset based on asset_id
        asset = get_object_or_404(AssetUsersAlaram, asset_id=asset_id)

        # Check if the user is in the asset's following group
        if user in asset.members.all():
            # Remove the user from the asset's following group
            asset.members.remove(user)
            return Response({'message': f'User {user.username} removed from members group.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': f'User {user.username} not in members group.'}, status=status.HTTP_400_BAD_REQUEST)
