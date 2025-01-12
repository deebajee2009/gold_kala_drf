from django.db import models
from django.contrib.auth.models import User

# Model to store the fixed price of gold (assumed to be constant)
class GoldPrice(models.Model):
    price_per_gram = models.DecimalField(max_digits=10,)  # Price per gram of gold
    date = models.DateTimeField(auto_now_add=True)  # Timestamp when the price is set
    
    def __str__(self):
        return f"Gold price: {self.price_per_gram} per gram"

# Model to track the balance of gold and money for each user
class UserBalance(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    balance_gold = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # User's gold balance
    balance_rial = models.DecimalField(max_digits=10, default=0)  # User's money balance
    date =  models.DateTimeField(auto_now_add=True)  # Timestamp of the balance
    
    class Meta:
        ordering = ['-balance_date']  # Sort by balance_date in descending 
    
    def __str__(self):
        return f"{self.user_id} Balance - Gold: {self.balance_gold} grams, Money: {self.balance_rial}"

# Model to track gold transactions (buying and selling)
class GoldTransaction(models.Model):
    BUY = 'buy'
    SELL = 'sell'
    COMPLETED = 'completed'
    FAILURE = 'failure' 
    
    TRANSACTION_TYPES = [
        (BUY, 'Buy'), 
        (SELL, 'Sell')
    ]
    STATUS_TYPES = [
        (COMPLETED, 'Completed'),
        (FAILURE, 'Failure')
    ]
    
    transaction_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # User performing the transaction
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)  # Type of transaction (buy or sell)
    gold_weight_gram = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of gold transacted
    amount_rial = models.DecimalField(max_digits=10, decimal_places=2)  # Money paid/received in the transaction
    date = models.DateTimeField(auto_now_add=True)  # Timestamp of the transaction
    status = models.CharField(max_length=20, choices=STATUS_TYPES) # Status of transaction (completed or failure)
    def __str__(self):
        return f"{self.user_id} - {self.type} {self.gold_weight_gram}g at {self.amount_rial} amount"
