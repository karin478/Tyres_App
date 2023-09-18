from django.apps import AppConfig

class TyresAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Tyres_App'

    def ready(self):
        import Tyres_App.signals
