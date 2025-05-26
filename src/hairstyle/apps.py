from django.apps import AppConfig


class HairstyleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hairstyle"
    
    def ready(self):
        import hairstyle.signals
