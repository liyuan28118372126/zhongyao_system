"""Image recognition app configuration."""

from django.apps import AppConfig


class ImageRecognitionConfig(AppConfig):
    """Image recognition app config."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.image_recognition'
    verbose_name = '中药图像识别'
