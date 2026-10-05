from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
