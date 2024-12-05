from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Order  # Ajusta según tu modelo de Orden

@receiver(post_save, sender=Order)
def notify_new_order(sender, instance, created, **kwargs):
    if created:  # Solo si es una nueva orden
        channel_layer = get_channel_layer()
        
        # Preparar los datos de la notificación
        notification_data = {
            'id': instance.id,
            'total': str(instance.total),  # Ajusta según tus campos
            'customer': str(instance.customer),  # Ajusta según tus campos
            'date': instance.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Ajusta según tus campos
        }
        
        # Enviar la notificación a través de WebSocket
        async_to_sync(channel_layer.group_send)(
            "admin_notifications",
            {
                "type": "send_notification",
                "message": f"Nueva orden #{instance.id} recibida",
                "data": notification_data
            }
        ) 