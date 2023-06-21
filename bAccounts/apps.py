from django.apps import AppConfig


class BaccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bAccounts'

    def ready(self):
        import bAccounts.signals