from django.apps import apps
from decimal import Decimal

def calculate_price(base_price, restaurant_tax, user=None):
    """
    Calcula el precio final basado en el usuario y la configuración
    """
    Configuration = apps.get_model('api', 'Configuration')
    config = Configuration.objects.first()
    
    # Calcular precio con impuesto del restaurante
    price_with_tax = Decimal(base_price) * (1 + (Decimal(restaurant_tax) / Decimal(100)))
    
    return round(price_with_tax, 2)
    # # Si el usuario está autenticado y es de Cuba (+53), devolver precio en CUP
    # if user and user.is_authenticated:
    #     if user.phone.startswith('+53'):
    
    # # Para otros usuarios, convertir a USD
    # return round(price_with_tax / Decimal(config.exchange_rate), 2)