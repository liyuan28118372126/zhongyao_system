"""Image recognition URLs."""

from django.urls import path
from . import views

app_name = 'image_recognition'

urlpatterns = [
    path('', views.recognize, name='recognize'),
]
