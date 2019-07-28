from django.contrib import admin, messages

# Register your models here.
from django.core import serializers
from django.http import HttpResponse

from blogapp.models import *

admin.site.site_title = '汪春旺博客网站'
admin.site.site_header = '汪春旺个人博客后台管理系统'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
    list_per_page = 10
    list_display_links = ['id', 'code']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
    list_per_page = 10
    list_display_links = ['id', 'code']


@admin.register(Recom)
class RecomAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
    list_per_page = 10
    list_display_links = ['id', 'code']


@admin.register(Artical)
class ArticalAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'views', 'create_time']
    list_per_page = 10
    list_display_links = ['id', 'title']
    search_fields = ['title', 'body']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_info', 'img', 'link_url', 'is_active']
    list_per_page = 10
    list_display_links = ['id', 'text_info']
    actions = ['enable', 'disable']

    # action方法
    def enable(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, '启用成功！', messages.SUCCESS)

    enable.short_description = '设为启用'

    def disable(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, '禁用成功！', messages.WARNING)
        # resp = HttpResponse(content_type='application/json')
        # serializers.serialize('json', queryset, stream=resp)
        # return resp

    disable.short_description = '设为禁用'

    # 符合条件过滤出action
    def get_actions(self, request):
        actions = super(BannerAdmin, self).get_actions(request)
        if request.user.username[0].upper() != 'A':
            if 'disable' in actions:
                del actions['disable']
        return actions


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'link_url']
    list_per_page = 10
    list_display_links = ['id', 'name']
