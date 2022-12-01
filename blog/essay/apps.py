from django.apps import AppConfig


class EssayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'essay'
    verbose_name = verbose_name_plural = '文章'
