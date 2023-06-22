from django.apps import AppConfig


class BiodataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'biodata'

    def ready(self):
        import biodata.signals
