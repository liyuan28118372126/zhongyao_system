"""Image recognition admin configuration."""

from django.contrib import admin
from .models import RecognitionRecord, MedicineImage


@admin.register(RecognitionRecord)
class RecognitionRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'confidence')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)


@admin.register(MedicineImage)
class MedicineImageAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'description')
    search_fields = ('medicine__name', 'description')
