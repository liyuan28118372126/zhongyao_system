"""News models."""

from django.db import models


class News(models.Model):
    """新闻模型。"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='作者')
    source = models.CharField(max_length=100, blank=True, null=True, verbose_name='来源')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='发布日期')
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name='图片')
    is_published = models.BooleanField(default=True, verbose_name='是否发布')

    class Meta:
        verbose_name = '新闻'
        verbose_name_plural = '新闻'

    def __str__(self):
        return self.title


class Category(models.Model):
    """新闻分类模型。"""
    name = models.CharField(max_length=50, unique=True, verbose_name='名称')

    class Meta:
        verbose_name = '新闻分类'
        verbose_name_plural = '新闻分类'

    def __str__(self):
        return self.name


class NewsCategory(models.Model):
    """新闻分类关联模型。"""
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='新闻')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')

    class Meta:
        verbose_name = '新闻分类关联'
        verbose_name_plural = '新闻分类关联'

    def __str__(self):
        return f"{self.news.title} - {self.category.name}"
