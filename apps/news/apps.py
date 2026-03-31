"""News app configuration."""

from django.apps import AppConfig


class NewsConfig(AppConfig):
    """News app config."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.news'
    verbose_name = '药闻'
