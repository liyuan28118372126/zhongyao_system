"""Medicine models."""

from django.db import models


class Medicine(models.Model):
    """中药材模型。"""
    name = models.CharField(max_length=100, unique=True, verbose_name='名称')
    latin_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='拉丁名')
    category = models.CharField(max_length=50, blank=True, null=True, verbose_name='分类')
    origin = models.CharField(max_length=100, blank=True, null=True, verbose_name='产地')
    properties = models.TextField(blank=True, null=True, verbose_name='性味归经')
    functions = models.TextField(blank=True, null=True, verbose_name='功效')
    indications = models.TextField(blank=True, null=True, verbose_name='主治')
    usage = models.TextField(blank=True, null=True, verbose_name='用法用量')
    precautions = models.TextField(blank=True, null=True, verbose_name='注意事项')
    image = models.URLField(blank=True, max_length=500, null=True, verbose_name='图片')

    class Meta:
        verbose_name = '中药材'
        verbose_name_plural = '中药材'

    def __str__(self):
        return self.name


class Prescription(models.Model):
    """方剂模型。"""
    name = models.CharField(max_length=100, unique=True, verbose_name='名称')
    ingredients = models.TextField(verbose_name='组成')
    dosage = models.TextField(blank=True, null=True, verbose_name='用量')
    preparation = models.TextField(blank=True, null=True, verbose_name='制法')
    functions = models.TextField(blank=True, null=True, verbose_name='功效')
    indications = models.TextField(blank=True, null=True, verbose_name='主治')
    precautions = models.TextField(blank=True, null=True, verbose_name='注意事项')
    image = models.URLField(blank=True, max_length=500, null=True, verbose_name='图片')

    class Meta:
        verbose_name = '方剂'
        verbose_name_plural = '方剂'

    def __str__(self):
        return self.name


class DietaryTherapy(models.Model):
    """药膳食疗模型。"""
    name = models.CharField(max_length=100, unique=True, verbose_name='名称')
    ingredients = models.TextField(verbose_name='原料')
    preparation = models.TextField(blank=True, null=True, verbose_name='制法')
    functions = models.TextField(blank=True, null=True, verbose_name='功效')
    indications = models.TextField(blank=True, null=True, verbose_name='适用症')
    precautions = models.TextField(blank=True, null=True, verbose_name='注意事项')
    image = models.URLField(blank=True, max_length=500, null=True, verbose_name='图片')

    class Meta:
        verbose_name = '药膳食疗'
        verbose_name_plural = '药膳食疗'

    def __str__(self):
        return self.name


class AcupuncturePoint(models.Model):
    """针灸穴位模型。"""
    name = models.CharField(max_length=100, unique=True, verbose_name='名称')
    location = models.TextField(blank=True, null=True, verbose_name='定位')
    functions = models.TextField(blank=True, null=True, verbose_name='功效')
    indications = models.TextField(blank=True, null=True, verbose_name='主治')
    acupuncture_method = models.TextField(blank=True, null=True, verbose_name='刺灸法')
    precautions = models.TextField(blank=True, null=True, verbose_name='注意事项')
    image = models.URLField(blank=True, max_length=500, null=True, verbose_name='图片')

    class Meta:
        verbose_name = '针灸穴位'
        verbose_name_plural = '针灸穴位'

    def __str__(self):
        return self.name
