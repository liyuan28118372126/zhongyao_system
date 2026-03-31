"""Sales app configuration."""

from django.apps import AppConfig


class SalesConfig(AppConfig):
    """Sales app config."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sales'
    verbose_name = '药材销售'
