from django.apps import AppConfig


class DirectorioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'directorio'

    def ready(self):
        import directorio.signals  # Importa las señales
