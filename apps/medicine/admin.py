"""Medicine admin configuration."""

from django.contrib import admin
from .models import Medicine, Prescription, DietaryTherapy, AcupuncturePoint


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'latin_name', 'category', 'origin')
    search_fields = ('name', 'latin_name', 'functions', 'indications')
    list_filter = ('category', 'origin')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'functions')
    search_fields = ('name', 'ingredients', 'functions', 'indications')


@admin.register(DietaryTherapy)
class DietaryTherapyAdmin(admin.ModelAdmin):
    list_display = ('name', 'functions')
    search_fields = ('name', 'ingredients', 'functions', 'indications')


@admin.register(AcupuncturePoint)
class AcupuncturePointAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location', 'functions', 'indications')
