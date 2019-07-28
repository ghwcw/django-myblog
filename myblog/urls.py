"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blogapp/', include('blogapp.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.views import static

from blogapp.models import Artical
from blogapp.views import Test
from myblog import settings

info_dict = {
    'queryset': Artical.objects.all(),
    'date_field': 'create_time',
}

urlpatterns = [

    path('admin/doc', include('django.contrib.admindocs.urls')),
    path('admin', admin.site.urls),
    path('ueditor', include('extraapps.DjangoUeditor.urls')),  # 添加DjangoUeditor的URL
    re_path('^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),  # Ueditor富文本上传图片，不支持path新方法！

    # blogapp URL
    path('', include('blogapp.urls')),

    # 测试
    path('test', Test.as_view(), name='test'),

    # 站点地图(快捷方法)
    path('sitemap/artical', sitemap,
         {'sitemaps': {'artical': GenericSitemap(info_dict, priority=0.6, changefreq='never')}},
         name='django.contrib.sitemaps.views.sitemap'),

]
