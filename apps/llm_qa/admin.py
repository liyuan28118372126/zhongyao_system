"""LLM QA admin configuration."""

from django.contrib import admin
from .models import QuestionAnswer


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'model_used', 'created_at')
    list_filter = ('created_at', 'model_used')
    search_fields = ('question', 'answer', 'user__username')
    readonly_fields = ('created_at',)
