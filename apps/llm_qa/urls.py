"""LLM QA URLs."""

from django.urls import path
from . import views

app_name = 'llm_qa'

urlpatterns = [
    path('', views.ask_question, name='ask_question'),
    path('clear-history/', views.clear_history, name='clear_history'),
    path('delete-history/', views.delete_history, name='delete_history'),
]
