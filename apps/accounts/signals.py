from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import get_user_model

from .models import UserWallet
from apps.asset_trade.models import AssetUsersAlaram


User = get_user_model()

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    """
    Signal that creates a Wallet for the user when a new user is created.
    """
    if created:  # Check if the user is newly created
        UserWallet.objects.create(user_id=instance)
