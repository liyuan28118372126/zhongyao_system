"""Sales admin configuration."""

from django.contrib import admin
from .models import Supply, Demand


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'specification', 'price', 'quantity', 'origin')
    list_filter = ('origin',)
    search_fields = ('medicine_name', 'specification')


@admin.register(Demand)
class DemandAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'specification', 'price', 'quantity', 'origin')
    list_filter = ('origin',)
    search_fields = ('medicine_name', 'specification')
