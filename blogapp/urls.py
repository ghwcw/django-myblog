#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2019-05-25
    Project : myblog
   FileName : urls.py
Description : 
-------------------------------------------------------------
"""
from django.urls import path
from blogapp.views import *

app_name = 'blogapp'

urlpatterns = [
    # 首页
    path('', IndexView.as_view(), name='index'),

    # 文章分类菜单，显示该分类下所有文章列表。需注意url冲突。
    path('<str:catecode>-list', ArticalListView.as_view(), name='article_list'),
    # 文章详情
    path('<str:catecode>/<int:pk>', ArticalDetailView.as_view(), name='article_detail'),
    # 标签
    path('tag/<str:tagcode>-list', TagView.as_view(), name='tag_article_list'),
    # 搜索关键字
    path('search', SearchView.as_view(), name='search'),
    # 关于博主
    path('about', AboutView.as_view(), name='about'),

]


