"""Medicine app configuration."""

from django.apps import AppConfig


class MedicineConfig(AppConfig):
    """Medicine app config."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.medicine'
    verbose_name = '中药材资料'
