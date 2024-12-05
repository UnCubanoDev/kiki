from django.core.management.base import BaseCommand
from api.models import OrderDetail, Configuration

class Command(BaseCommand):
    help = 'Populate historical prices for existing orders'

    def handle(self, *args, **kwargs):
        config = Configuration.objects.first()
        exchange_rate = config.exchange_rate if config else 1

        for detail in OrderDetail.objects.filter(unit_price=0):
            detail.unit_price = detail.product.price
            detail.tax_rate = detail.product.restaurant.tax
            detail.exchange_rate = exchange_rate
            detail.save()
            
        self.stdout.write(
            self.style.SUCCESS('Successfully populated historical prices')
        ) 