from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.cache import cache

from .models import Asset, AssetPrice
from .kafka_producer import publisher
from .models import AssetUsersAlaram

@receiver(post_save, sender=AssetPrice)
def my_model_pre_save(sender, instance, **kwargs):
    changed = instance.has_changed_from_last()
    if changed:
        asset_id = instance.asset_id
        asset_price = instance.price
        asset_unit = instance.unit
        if asset_members:
            # Simulate gold price update
            price_update = {
                "price": asset_price,
                 "asset_id": asset_id,
                 "unit": asset_unit
            }
            publisher.publish_price(price_update)

@receiver(post_save, sender=Asset)
def create_asset_alaram(sender, instance, created, **kwargs):
    """
    Signal that creates a Asset alram record for the asset when a new asset is created.
    """
    if created:  # Check if the user is newly created
        AssetUsersAlaram.objects.create(asset_id=instance)


@receiver(m2m_changed, sender=AssetUsersAlaram.members.through)
def members_added(sender, instance, action, reverse, pk_set, **kwargs):
    """
    This signal is triggered when the Many-to-Many field 'members' of a AssetUsersAlaram is changed.
    """

    if action == 'post_add':  # 'post_add' is triggered after adding new members
        # pk_set contains the primary keys of the members added
        asset_id = instance.asset_id
        current_list = cache.get(key)

        # If the list does not exist in cache, initialize an empty list
        if current_list is None:
            current_list = []
        for user_id in pk_set:
            if not user_id in current_list:
                current_list.append(user_id)
        cache.set(asset_id, current_list)

    if action == 'post_remove':
        asset_id = instance.asset_id
        current_list = cache.get(key)

        for user_id in pk_set:
            if user_id in current_list:
                current_list.remove(user_id)
        cache.set(asset_id, current_list)
