from django.apps import AppConfig


class HairstyleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hairstyle"
    
    def ready(self):
        import hairstyle.signals
        try:
            from .scheduler import start_scheduler
            start_scheduler()
        except Exception as e:
            print(f"Error starting scheduler: {e}")
