from django.db import models
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey
from django_jalali.db import models as jmodels

from apps.accounts.models import UserWallet


User = settings.AUTH_USER_MODEL

class Asset(MPTTModel):
    """
    Model for saving object of asset_trade

    attributes:
        name: name of asset like dollar or bitcoin
        parent: name of parent of asset like metals or crypto-currencies
    """
    asset_id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        unique=True
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class AssetPrice(models.Model):
    """
    Model for saving price of asset after external API fetch by celery task

    attributes:
        asset_id: asset of the price
        date: date of asset price value
        time: time of asset price value
        price: the value of price
        unit: unit of price like Toman or Dollar
    """
    asset_price_id = models.BigAutoField(primary_key=True)
    asset_id = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='prices'
    )
    date = jmodels.jDateField()
    time = models.TimeField()
    price = models.BigIntegerField()
    unit = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = jmodels.jManager()

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.asset.name}'s price is {self.price} at {self.date}-{self.time}"

    def has_changed_from_last(self):
        """
        Compares the current instance with the last saved instance (based on created_at).
        Returns a dictionary of changed fields or an empty dictionary if no changes.
        Handles the case where there are no previous records.
        """
        try:
            last_record = AssetPrice.objects.exclude(pk=self.pk).order_by('-created_at')[0]  # Exclude self to prevent comparing with it self
            changed_fields = {}

            for field in self._meta.fields:
                field_name = field.name
                if field_name == 'price':
                    current_value = getattr(self, field_name)
                    last_value = getattr(last_record, field_name)
                    if current_value != last_value:
                        changed_fields[field_name] = {'old': last_value, 'new': current_value}

            return changed_fields
        except AssetPrice.DoesNotExist:
            return {}  # No previous records


class AssetlBalance(MPTTModel):
    """
    Model for saving balance amount of asset belonging to a Wallet

    attributes:
        wallet_id: id of user wallet that has this asset balance
        asset_id: id of asset
        balance_asset: amount of asset that user has
        date: date of having that asset
    """
    balance_id = models.BigAutoField(primary_key=True)
    wallet_id = models.ForeignKey(
        UserWallet,
        on_delete=models.CASCADE,
        related_name='wallet_balance'
    )
    asset_id = TreeForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='asset_balance'
    )
    balance_asset = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )  # User's gold balance
    date = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        ordering = ['-date']
    def __str__(self):
        return f"{str(self.asset_id)} balance: {str(self.balance_asset)}"


# Model to track asset transactions (buying and selling)
class AssetTransaction(MPTTModel):
    """
    Model for saving asset buying and selling transactions

    attributes:
        user_id: id of user that has done transaction
        asset_id: id of asset that traded
        type: define selling or buying
        asset_amount: amount of asset that traded
        amount_toman: money amount that has expended for trade
        asset_price: price of asset that traded
        date: date of transaction
        status: set completeness of transaction operation
    """
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
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )  # User performing the transaction
    asset_id = TreeForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )  # Type of transaction (buy or sell)
    asset_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )  # Amount of gold transacted
    amount_toman = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )  # Money paid/received in the transaction
    asset_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    date = jmodels.jDateTimeField() # Timestamp of the transaction
    status = models.CharField(
        max_length=20,
        choices=STATUS_TYPES
    ) # Status of transaction (completed or failure)

    objects = jmodels.jManager()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user_id} - {self.type} {self.asset_amount} at {self.amount_toman} amount"


class AssetUsersAlaram(MPTTModel):
    """
    Model for saving user following members of asset for notif handling

    attributes:
        asset_id: id of asset
        members: users that want to be notified of asset price change
    """
    asset_id = TreeForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='user_alaram'
    )
    members = models.ManyToManyField(
        User,
        blank=True
    )

    class MPTTMeta:
        order_insertion_by = ['-asset_id']

    def __str__(self):
        # Limit to showing only the first 3 authors, for example
        members = ', '.join([member.username for member in self.members.all()[:3]])  # Limit to first 3 authors
        if self.members.count() > 3:
            return f"{self.asset_id} has {members}, and others"
        return f"{self.asset_id} has {members}"
