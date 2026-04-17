from django.apps import AppConfig


class GeopramAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "geopram_app"

    def ready(self):
        import geopram_app.signals
