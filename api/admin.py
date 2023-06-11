from django.contrib import admin
from .models import Articulo, Cliente, Destinatario, Paquete


# Register your models here.
@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    pass

@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    pass

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    pass

@admin.register(Destinatario)
class DestinatarioAdmin(admin.ModelAdmin):
    pass
