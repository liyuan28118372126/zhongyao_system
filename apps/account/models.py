"""Account models."""

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """User profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True, verbose_name='头像')
    bio = models.TextField(blank=True, null=True, verbose_name='个人简介')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='联系电话')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return self.user.username
