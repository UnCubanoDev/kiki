from django.apps import apps

def calculate_price(base_price, restaurant_tax, user=None):
    """
    Calcula el precio final basado en el usuario y la configuración
    """
    Configuration = apps.get_model('api', 'Configuration')
    config = Configuration.objects.first()
    
    if not config or not user:
        return base_price
        
    # Calcular precio con impuesto del restaurante
    price_with_tax = base_price * (1 + (restaurant_tax / 100))
    
    # Si es usuario de Cuba (+53), devolver precio en CUP
    if user.phone.startswith('+53'):
        return round(price_with_tax, 2)
    
    # Para otros usuarios, convertir a USD
    return round(price_with_tax / config.exchange_rate, 2) 