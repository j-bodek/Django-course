from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # connect signals so django will know about them 
    def ready(self):
        import users.signals
