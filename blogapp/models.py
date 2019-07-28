from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.html import format_html

from extraapps.DjangoUeditor.models import UEditorField


class Category(models.Model):
    """
    文章分类字典表
    """
    code = models.CharField(verbose_name='分类编码', max_length=4, unique=True)
    name = models.CharField(verbose_name='分类名称', max_length=20)
    index = models.IntegerField(verbose_name='排序', default=999)

    class Meta:
        verbose_name = '文章分类字典表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签字典表
    """
    code = models.CharField(verbose_name='标签编码', max_length=4, unique=True)
    name = models.CharField(verbose_name='标签名称', max_length=20)

    class Meta:
        verbose_name = '标签字典表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Recom(models.Model):
    """
    推荐位字典表
    """
    code = models.CharField(verbose_name='推荐位编码', max_length=4, unique=True)
    name = models.CharField(verbose_name='推荐位', max_length=20)

    class Meta:
        verbose_name = '推荐位字典表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Artical(models.Model):
    """
    博客文章表
    """
    title = models.CharField(verbose_name='标题', max_length=100)
    category = models.ForeignKey(verbose_name='分类id', to=Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    tags = models.ManyToManyField(verbose_name='标签id', to=Tag, blank=True)
    img = models.ImageField(verbose_name='文章图片', upload_to='artical-img/%Y-%m', blank=True, null=True)
    excerpt = models.CharField(verbose_name='摘要', max_length=100, blank=True, null=True)
    # Ueditor是百度开发的一个富文本编辑器，功能强大。用富文本编辑body
    body = UEditorField(verbose_name='内容', width=800, height=500, imagePath='up-img/', filePath='up-file/',
                        upload_settings={'imageMaxSize': 1204000}, blank=True, null=True)
    user = models.ForeignKey(verbose_name='作者id', to=User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(verbose_name='浏览量', default=0)
    recom = models.ForeignKey(verbose_name='推荐位id', to=Recom, on_delete=models.DO_NOTHING, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modi_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        verbose_name = '博客文章表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', urlconf='blogapp.urls', args=(self.category_id, self.pk,))


class Banner(models.Model):
    """
    轮播图片表
    """
    text_info = models.CharField(verbose_name='标题', max_length=50, default='')
    img = models.ImageField(verbose_name='轮播图片', upload_to='banner/')
    link_url = models.URLField(verbose_name='图片链接', max_length=100)
    is_active = models.BooleanField(verbose_name='是否可用', default=False)

    def link_url_color(self):
        """
        根据状态，给字段添加CSS颜色显示
        :return:
        """
        if self.is_active is True:
            f_color = 'green'
        else:
            f_color = 'gray'
        return format_html('<span style="color: {}">{}</span>', f_color, self.link_url)

    class Meta:
        verbose_name = '轮播图表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.text_info


class Link(models.Model):
    """
    友情链接表
    """
    name = models.CharField(verbose_name='链接名称', max_length=20)
    link_url = models.URLField(verbose_name='网址', max_length=100)

    class Meta:
        verbose_name = '友情链接表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
