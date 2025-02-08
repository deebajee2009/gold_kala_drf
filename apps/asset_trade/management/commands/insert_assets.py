from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from apps.asset_trade.models import Asset

class Command(BaseCommand):
    help = 'Check if data exists in the database, and if not, insert it'

    def handle(self, *args, **kwargs):

        try:
            # Insert the data if it doesn't exist
            Metal, created = Asset.objects.get_or_create(name='فلزات گران بها')
            Currency, created = Asset.objects.get_or_create(name='ارز')
            Crypto, created = Asset.objects.get_or_create(name='رمزارز')
            Dollar, created = Asset.objects.get_or_create(name='دلار', parent=Currency)
            Gold, created = Asset.objects.get_or_create(name='گرم طلای 18 عیار', parent=Metal)
            Bitcoin, created = Asset.objects.get_or_create(name='بیت کوین', parent=Crypto)
            Ethereum, created = Asset.objects.get_or_create(name='اتریوم', parent=Crypto)
            self.stdout.write(self.style.SUCCESS('Data inserted successfully'))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Error inserting data: {e}'))
