from io import BytesIO

from django.core import paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from blogapp.models import *


def get_globalvars(request):
    # 查询文章分类导航
    cates = Category.objects.all()[:5]
    # 热门推荐，根据推荐字典取R02
    reco2_articals = Artical.objects.filter(recom__code='R02').order_by('-create_time')[:4]
    # 所有标签
    tags = Tag.objects.all()
    return locals()


class IndexView(View):
    """
    首页视图
    """

    def get(self, request):
        # # 查询文章分类导航
        # cates = Category.objects.all()[:5]
        # # 热门推荐，根据推荐字典取R02
        # reco2_articals = Artical.objects.filter(recom__code='R02').order_by('-create_time')[:4]
        # # 所有标签
        # tags = Tag.objects.all()

        # 轮播图
        banners = Banner.objects.filter(is_active=True)[:4]

        # 首页推荐阅读
        reco_articals = Artical.objects.filter(recom__code='R01').order_by('-create_time')[:3]
        # 最新文章
        latest_articals = Artical.objects.order_by('-create_time')[:5]
        # 热门文章，按浏览量
        hot_articals = Artical.objects.order_by('-views')[:5]

        # 友情链接
        links = Link.objects.all()

        context = {
            # 'cates': cates,
            'banners': banners,
            'reco_articals': reco_articals,
            'latest_articals': latest_articals,
            'hot_articals': hot_articals,
            # 'reco2_articals': reco2_articals,
            # 'tags': tags,
            'links': links,
        }
        context.update(get_globalvars(request))
        return render(request=request, template_name='blogapp/index.html', context=context)


class ArticalListView(View):
    """
    不同分类的文章列表
    """

    def get(self, request, catecode):
        # # 查询文章分类导航
        # cates = Category.objects.all()[:5]
        # # 热门推荐，根据推荐字典取R02
        # reco2_articals = Artical.objects.filter(recom__code='R02').order_by('-create_time')[:4]
        # # 所有标签
        # tags = Tag.objects.all()

        # 获取文章列表
        articals = Artical.objects.filter(category__code=catecode).order_by('-create_time')
        # 获取分类
        cate = Category.objects.get(code=catecode)

        # 分页
        pn = paginator.Paginator(articals, per_page=2)  # 实例化分页器对象
        page_num = request.GET.get('page')  # 获取当前页码
        try:
            page_list_obj = pn.page(page_num)  # 进行分页，返回数据列表（将之传给模板）
        except paginator.PageNotAnInteger:
            page_list_obj = pn.page(1)
        except paginator.InvalidPage:
            page_list_obj = pn.page(pn.num_pages)

        context = {
            'cate': cate,
            'page_list_obj': page_list_obj,
            # 'reco2_articals': reco2_articals,
            # 'tags': tags,
            # 'cates': cates,
            'catecode': catecode,
        }
        context.update(get_globalvars(request))

        return render(request=request, template_name='blogapp/list.html', context=context)


class ArticalDetailView(View):
    """
    文章详情页
    """

    def get(self, request, catecode, pk):
        # # 查询文章分类导航
        # cates = Category.objects.all()[:5]
        # # 热门推荐，根据推荐字典取R02
        # reco2_articals = Artical.objects.filter(recom__code='R02').order_by('-create_time')[:4]
        # # 所有标签
        # tags = Tag.objects.all()

        # 可能感兴趣文章
        interest_articals = Artical.objects.filter(category__code=catecode).exclude(pk=pk).order_by('?')[:5]
        # 要显示详情的文章
        this_artical = Artical.objects.get(pk=pk)
        # 上一篇
        pre_artical = Artical.objects.filter(create_time__gt=this_artical.create_time, category__code=catecode).first()
        # 下一篇
        next_artical = Artical.objects.filter(create_time__lt=this_artical.create_time, category__code=catecode).last()
        # 浏览量+1
        this_artical.views += 1
        this_artical.save()
        context = locals()
        context.update(get_globalvars(request))
        return render(request=request, template_name='blogapp/show.html', context=context)


class TagView(View):
    """
    按标签显示文章列表
    """

    def get(self, request, tagcode):
        # # 查询文章分类导航
        # cates = Category.objects.all()[:5]
        # # 热门推荐，根据推荐字典取R02
        # reco2_articals = Artical.objects.filter(recom__code='R02').order_by('-create_time')[:4]
        # # 所有标签
        # tags = Tag.objects.all()

        # 根据标签查询文章列表
        tag_articals = Artical.objects.filter(tags__code=tagcode).order_by('-create_time')
        # 获取标签名
        tag_name = Tag.objects.get(code=tagcode)

        # 分页
        pn = paginator.Paginator(tag_articals, 2)  # 实例化分页器对象
        page_num = request.GET.get('page')  # 获取当前页码
        try:
            page_list_obj = pn.page(page_num)  # 进行分页，返回数据列表（将之传给模板）
        except paginator.PageNotAnInteger:
            page_list_obj = pn.page(1)
        except paginator.InvalidPage:
            page_list_obj = pn.page(pn.num_pages)
        context = locals()
        context.update(get_globalvars(request))
        return render(request=request, template_name='blogapp/tags.html', context=context)


class SearchView(View):
    """
    按标题或内容关键字搜索文章
    """

    def get(self, request):
        # # 查询文章分类导航
        # cates = Category.objects.all()[:5]
        # # 热门推荐，根据推荐字典取R02
        # reco2_articals = Artical.objects.filter(recom__code='R02').order_by('-create_time')[:4]
        # # 所有标签
        # tags = Tag.objects.all()

        # 获取关键字
        keyword = request.GET.get('keyword', '')
        if keyword:
            search_articles = Artical.objects.filter(Q(title__icontains=keyword) | Q(body__icontains=keyword))
        else:
            search_articles = Artical.objects.order_by('-create_time')

        # 分页
        pn = paginator.Paginator(search_articles, 4)  # 实例化分页器对象
        page_num = request.GET.get('page')  # 获取当前页码
        try:
            page_list_obj = pn.page(page_num)  # 分页，返回数据列表
        except paginator.PageNotAnInteger:
            page_list_obj = pn.page(1)
        except paginator.InvalidPage:
            page_list_obj = pn.page(pn.num_pages)
        context = locals()
        context.update(get_globalvars(request))
        return render(request, template_name='blogapp/search.html', context=context)


class AboutView(View):
    """
    关于页
    """

    def get(self, request):
        # 查询文章分类导航
        cates = Category.objects.all()[:5]

        return render(request, template_name='blogapp/about.html', context={'cates': cates})


class Test(View):
    """
    测试
    """
    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

        buffer = BytesIO()
        c = Canvas(buffer)
        pdfmetrics.registerFont(TTFont('simsun', 'simsun.ttc'))     # 支持中文
        Canvas.setFont(c, "simsun", 12)
        c.drawString(0, 500, '使用ReportLab创建复杂的PDF文档时，可以考虑使用io库作为PDF文件的临时保存地点。这个库提供了一个类似于文件的对象接口，非常实用。 下面的例子是上面的“Hello World”示例采用io重写后的样子：')
        c.showPage()
        c.save()
        pdf = buffer.getvalue()
        response.write(pdf)
        buffer.close()

        return response



