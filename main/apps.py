from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        # Import our signal handlers
        from . import signals  # noqa: F401
