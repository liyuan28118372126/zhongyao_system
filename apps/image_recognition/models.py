"""Image recognition models."""

from django.db import models
from django.contrib.auth.models import User


class RecognitionRecord(models.Model):
    """识别记录模型。"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='recognition_uploads/')
    result = models.JSONField(blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recognition {self.id} by {self.user.username if self.user else 'Anonymous'}"


class MedicineImage(models.Model):
    """药材图像库模型。"""
    medicine = models.ForeignKey('medicine.Medicine', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='medicine_images/')
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Image of {self.medicine.name}"
