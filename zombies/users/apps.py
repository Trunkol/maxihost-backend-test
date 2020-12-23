from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    
    def ready(self):
        try:
            from . import signals  # noqa F401
        except ImportError as e:
            raise e
