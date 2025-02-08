from django.contrib.auth.models import User
from django.db import transaction
from django.core.cache import cache

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema

from .models import Asset, AssetTransaction, AssetlBalance, UserWallet, AssetPrice
from .serializers import AssetTransactionSerializer, AssetPriceSerializer, AssetSerializer
import core


class BuyAssetView(APIView):
    """
    An APIView for handling request of Buying and its transactions
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=AssetTransactionSerializer)
    def post(self, request):
        # Input data is needed to modify before pass to serializer
        user_id = request.data.get('user_id')
        asset_id = request.data.get('asset_id')
        amount_toman = request.data.get('amount_toman')

        data = request.data.copy()
        data['type'] = AssetTransaction.BUY

        serializer = AssetTransactionSerializer(data=data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    transaction = serializer.save()

                    asset = Asset.objects.get(asset_id=asset_id)
                    user_wallet = UserWallet.objects.get(user_id=user_id)

                    asset_balance = AssetlBalance.objects.filter(wallet_id=user_id, asset_id=asset).last()

                    if not asset_object:
                        # If the last object exists, use it
                        asset_balance, created = AssetlBalance.objects.get_or_create(
                            wallet_id=user_id,
                            asset_id=asset,
                            defaults={'balance_asset': 0}
                        )

                    user_wallet.balance_toman = user_wallet.balance_toman - amount_toman
                    user_wallet.save()

                    asset_balance.balance_asset = asset_balance.balance_asset + transaction.asset_amount
                    asset_balance.balance_id = None
                    asset_balance.save()

                    return Response(
                        transaction.data,
                        status=status.HTTP_201_CREATED
                    )
            except IntegrityError:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class SellAssetView(APIView):
    """
    An APIView for Buying based on ACID Transactions
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=AssetTransactionSerializer)
    def post(self, request):
        # Input Bdata is needed to modify before pass to serializer
        user_id = request.data.get('user_id')
        asset_id = request.data.get('asset_id')
        asset_amount = request.data.get('asset_amount')

        data = request.data.copy()
        data['type'] = AssetTransaction.SELL

        serializer = AssetTransactionSerializer(data=data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    transaction = serializer.save()

                    asset = Asset.objects.get(asset_id=asset_id)
                    user_wallet = UserWallet.objects.get(user_id=user_id)
                    asset_balance = AssetlBalance.objects.filter(wallet_id=user_id, asset_id=asset).last()

                    user_wallet.balance_toman = user_wallet.balance_toman + transaction.amount_toman
                    user_wallet.save()

                    asset_balance.balance_asset = asset_balance.balance_asset - asset_amount
                    asset_balance.balance_id = None
                    asset_balance.save()

                    return Response(
                        transaction.data,
                        status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class MyModelPagination(PageNumberPagination):
    """
    A Paginator class for TransactionHistoryView
    """
    page_size = 10  # You can specify page size here, or rely on the global settings
    page_size_query_param = 'page_size'  # Allows clients to pass the page size as a query param
    max_page_size = 100  # Maximum number of items per page


class TransactionHistoryView(APIView):
    """
    An APIView for History of User transactions
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=AssetTransactionSerializer)
    def get(self, request, user_id):
        # Query all transactions for the user with the given user_id
        transactions = AssetTransaction.objects.filter(user_id=user_id)

        # If no transactions found, return a 404 response
        if not transactions.exists():
            return Response(
                {"detail": "No transactions found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Apply pagination
        paginator = MyModelPagination()
        paginated_queryset = paginator.paginate_queryset(transactions, request)

        # Serialize the transaction data
        serializer = AssetTransactionSerializer(paginated_queryset, many=True)

        # Return the serialized data
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class PriceView(generics.ListAPIView):
    """
    An ListAPIView for returning price details of all assets
    """
    queryset = Asset.objects.all()  # Or any filtered queryset
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=AssetSerializer)
    def list(self, request, *args, **kwargs):
        cached_data = cache.get('all_data')
        if cached_data:
            return Response(data)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
