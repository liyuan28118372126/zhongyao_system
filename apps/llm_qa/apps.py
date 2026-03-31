"""LLM QA app configuration."""

from django.apps import AppConfig


class LlmQaConfig(AppConfig):
    """LLM QA app config."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.llm_qa'
    verbose_name = '大模型答疑'
