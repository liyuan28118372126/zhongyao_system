"""Sales URLs."""

from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.index, name='index'),
    path('supply/list/', views.supply_list, name='supply_list'),
    path('supply/create/', views.create_supply, name='create_supply'),
    path('supply/<int:pk>/', views.supply_detail, name='supply_detail'),
    path('supply/<int:pk>/update/', views.update_supply, name='update_supply'),
    path('supply/<int:pk>/delete/', views.delete_supply, name='delete_supply'),
    path('demand/list/', views.demand_list, name='demand_list'),
    path('demand/create/', views.create_demand, name='create_demand'),
    path('demand/<int:pk>/', views.demand_detail, name='demand_detail'),
    path('demand/<int:pk>/update/', views.update_demand, name='update_demand'),
    path('demand/<int:pk>/delete/', views.delete_demand, name='delete_demand'),
    path('price/list/', views.price_list, name='price_list'),
    path('price/load/', views.load_price_data, name='load_price_data'),
]
