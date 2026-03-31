"""LLM QA models."""

from django.db import models
from django.contrib.auth.models import User


class QuestionAnswer(models.Model):
    """问答记录模型。"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='用户')
    question = models.TextField(verbose_name='问题')
    answer = models.TextField(blank=True, null=True, verbose_name='回答')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    model_used = models.CharField(max_length=100, blank=True, null=True, verbose_name='使用模型')

    class Meta:
        verbose_name = '问答记录'
        verbose_name_plural = '问答记录'

    def __str__(self):
        return f"问答 {self.id} by {self.user.username if self.user else '匿名'}"
