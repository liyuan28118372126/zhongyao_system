"""Medicine URLs."""

from django.urls import path
from . import views

app_name = 'medicine'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/<str:pk>/', views.medicine_detail, name='medicine_detail'),
    path('medicines/autocomplete/', views.medicine_autocomplete, name='medicine_autocomplete'),
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('prescriptions/autocomplete/', views.prescription_autocomplete, name='prescription_autocomplete'),
    path('dietary-therapies/', views.dietary_therapy_list, name='dietary_therapy_list'),
    path('dietary-therapies/<int:pk>/', views.dietary_therapy_detail, name='dietary_therapy_detail'),
    path('dietary-therapies/autocomplete/', views.dietary_therapy_autocomplete, name='dietary_therapy_autocomplete'),
    path('acupuncture-points/', views.acupuncture_point_list, name='acupuncture_point_list'),
    path('acupuncture-points/<int:pk>/', views.acupuncture_point_detail, name='acupuncture_point_detail'),
    path('acupuncture-points/autocomplete/', views.acupuncture_point_autocomplete, name='acupuncture_point_autocomplete'),
]
