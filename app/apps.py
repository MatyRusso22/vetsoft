from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    Clase de configuracion de la aplicacion
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
