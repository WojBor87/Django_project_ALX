from django.apps import AppConfig


class DevboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devboard'
    verbose_name = 'DevBoard - System zarządzania projektami'

    def ready(self):
        print('devboard ready!')
