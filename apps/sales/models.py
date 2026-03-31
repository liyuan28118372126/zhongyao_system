"""Sales models."""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Supply(models.Model):
    """供应信息模型。"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='用户')
    medicine = models.ForeignKey('medicine.Medicine', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='中药材')
    medicine_name = models.CharField(max_length=100, verbose_name='药材名称')
    specification = models.CharField(max_length=200, blank=True, null=True, verbose_name='规格')
    quantity = models.CharField(max_length=50, blank=True, null=True, verbose_name='供应数量')
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name='药材库存')
    origin = models.CharField(max_length=200, blank=True, null=True, verbose_name='药材产地')
    invoice_requirement = models.CharField(max_length=100, blank=True, null=True, verbose_name='票据需求')
    quality_requirement = models.CharField(max_length=100, blank=True, null=True, verbose_name='质量需求')
    qualification_requirement = models.CharField(max_length=100, blank=True, null=True, verbose_name='资质要求')
    sample = models.CharField(max_length=50, blank=True, null=True, verbose_name='寄样')
    payment = models.CharField(max_length=100, blank=True, null=True, verbose_name='付款')
    packaging = models.CharField(max_length=100, blank=True, null=True, verbose_name='包装')
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系电话')
    contact_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='联系人')
    update_time = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新时间')
    price = models.CharField(max_length=50, blank=True, null=True, verbose_name='售价')
    minimum_order = models.CharField(max_length=50, blank=True, null=True, verbose_name='起售量')
    # 市场价格字段
    bozhou_price = models.CharField(max_length=50, blank=True, null=True, verbose_name='亳州价格')
    angui_price = models.CharField(max_length=50, blank=True, null=True, verbose_name='安国价格')
    chengdu_price = models.CharField(max_length=50, blank=True, null=True, verbose_name='成都价格')
    yulin_price = models.CharField(max_length=50, blank=True, null=True, verbose_name='玉林价格')
    lianqiao_price = models.CharField(max_length=50, blank=True, null=True, verbose_name='廉桥价格')
    puning_price = models.CharField(max_length=50, blank=True, null=True, verbose_name='普宁价格')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '供应信息'
        verbose_name_plural = '供应信息'

    def __str__(self):
        return f"供应: {self.medicine_name}"



class Demand(models.Model):
    """求购信息模型。"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='用户')
    medicine_name = models.CharField(max_length=100, verbose_name='药材名称')
    specification = models.CharField(max_length=200, blank=True, null=True, verbose_name='规格')
    quantity = models.CharField(max_length=50, blank=True, null=True, verbose_name='求购数量')
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name='地区')
    origin = models.CharField(max_length=200, blank=True, null=True, verbose_name='产地要求')
    price = models.CharField(max_length=50, blank=True, null=True, verbose_name='价格')
    contact_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系电话')
    update_time = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新时间')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '求购信息'
        verbose_name_plural = '求购信息'

    def __str__(self):
        return f"求购: {self.medicine_name}"
