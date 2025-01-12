from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db import transaction

from .models import GoldTransaction, UserBalance, GoldPrice
from .serializers import GoldTransactionSerializer
import core

class BuyGoldView(APIView):
    def post(self, request):
        # Input data is needed to modify before pass to serializer
        data = request.data.copy()
        user_id = data.get('user_id')
        amount_rial = data.get('amount_rial') 
        data['amount_rial'] = amount_rial
        
        # Get gold price from utils in core module 
        gold_price = core.utils.get_current_gold_price()
        data['price_per_gram'] = gold_price
        
        # Set transaction type for savinf in DB model
        transaction_type = GoldTransaction.BUY
        data['type'] = transaction_type # Modify request data add transaction type
        
        # Calculate amount of Gold user can buy based on amount_rial
        gold_weight_gram = round((amount_rial / gold_price), 1)
        data['gold_weight_gram'] = gold_weight_gram # Modify request data add gold weight gram
        
        try:
            with transaction.atomic():
            
                serializer = GoldTransactionSerializer(data=data)
                if serializer.is_valid():

                    user_balance = UserBalance.objects.filter(user_id=user_id).last()
                    rial_balance =  user_balance.balance_rial - amount_rial
                    gold_balance = user_balance.balance_gold + gold_weight_gram
                    UserBalance.objects.create(
                        user_id=user_id, 
                        balance_gold=gold_balance, 
                        balance_rial=rial_balance
                    )
                    
                    transaction = serializer.save()
                    
                    return Response(
                        {
                            'transaction_id': transaction.transaction_id,
                            'user_id': user_id,
                            'amount_rial': transaction.amount_rial,
                            'gold_weight_gram': transaction.gold_weight_gram,
                            'price_per_gram': transaction.price_per_gram,
                            'status': transaction.status
                        },
                        status=status.HTTP_201_CREATED
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SellGoldView(APIView):
    def post(self, request):
        # Input data is needed to modify before pass to serializer
        data = request.data.copy()
        user_id = data.get('user_id')
        gold_weight_gram = data.get('gold_weight_gram') 
        
        # Get gold price from utils in core module 
        gold_price = core.utils.get_current_gold_price()
        data['price_per_gram'] = gold_price
        
        amount_rial = round(gold_price * gold_weight_gram)
        data['amount_rial'] = amount_rial
        
        # Set transaction type for savinf in DB model
        transaction_type = GoldTransaction.SELL
        data['transaction_type'] = transaction_type # Modify request data add transaction type
        
        try:
            with transaction.atomic():
                serializer = GoldTransactionSerializer(data=request.data)
                if serializer.is_valid():
                    user_balance = UserBalance.objects.filter(user_id=user_id).last()
                    rial_balance =  user_balance.balance_rial + amount_rial
                    gold_balance = user_balance.balance_gold - gold_weight_gram
                    UserBalance.objects.create(
                        user_id=user_id, 
                        balance_gold=gold_balance, 
                        balance_rial=rial_balance
                    )
                    
                    transaction = serializer.save()
                    
                    return Response(
                        {
                            'transaction_id': transaction.transaction_id,
                            'user_id': user_id,
                            'amount_rial': transaction.amount_rial,
                            'gold_weight_gram': transaction.gold_weight_gram,
                            'price_per_gram': transaction.price_per_gram,
                            'status': transaction.status
                        },
                        status=status.HTTP_201_CREATED
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserTransactionHistoryView(APIView):
    def get(self, request, user_id):
        # Query all transactions for the user with the given user_id
        transactions = GoldTransaction.objects.filter(user_id=user_id)

        # If no transactions found, return a 404 response
        if not transactions.exists():
            return Response({"detail": "No transactions found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the transaction data
        serializer = GoldTransaction(transactions, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)