from django.apps import AppConfig
from django.db import transaction  # For atomic operations


class AssetTradeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.asset_trade'  # The name of the app, in dot notation
    verbose_name = 'Asset Trade'  # A human-readable name for the app

    def ready(self):
        import apps.asset_trade.signals
        # from django_celery_beat.models import PeriodicTask, IntervalSchedule
        #
        # with transaction.atomic():
        #     schedule, created = IntervalSchedule.objects.update_or_create(
        #         every=60,
        #         period=IntervalSchedule.MINUTES,
        #     )
        #     PeriodicTask.objects.update_or_create(
        #         interval=schedule,
        #         name='Asset Price periodic task',
        #         defaults={'task': 'apps.asset_trade.tasks.fetch_and_update_cache'},
        #     )
