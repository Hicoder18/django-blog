from django.db import models
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField


# Create your models here.
class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    """文章主题或者说类别。"""
    name = models.CharField('分类名称', max_length=50)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE, null=True,
        blank=True, related_name='son')
    level = models.IntegerField(null=True, blank=True)
    top_parent = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        """返回模型的字符串表示"""
        return self.name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField('文章标签', max_length=30)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Essay(models.Model):
    """文章"""
    cate = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        verbose_name='分类', blank=True)
    title = models.CharField('文章标题', max_length=80)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    content = MDTextField('正文')  # mdeditor
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None,
        null=True, verbose_name='作者')
    views = models.PositiveIntegerField('阅读量', default=0)
    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title
