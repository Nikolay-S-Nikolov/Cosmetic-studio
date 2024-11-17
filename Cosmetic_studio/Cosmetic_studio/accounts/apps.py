from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Cosmetic_studio.accounts'

    def ready(self):
        import Cosmetic_studio.accounts.signals