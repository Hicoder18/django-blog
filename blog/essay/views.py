from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import markdown

from .models import Category, Essay, Tag
from .forms import EssayForm


# Create your views here.
def index(request):
    """博客主页"""
    cates = Category.objects.all()
    es = Essay.objects.all().order_by('-created_time')[0:10]
    context = {'categories': cates, 'articles': es}
    return render(request, 'essay/index.html', context)


def category(request):
    """显示所有主题"""
    cates = Category.objects.all()
    context = {'categories': cates}
    return render(request, 'essay/cates.html', context)


def cate(request, cate_id):
    """显示单个文章分类及其所有文章"""
    cate = Category.objects.get(id=cate_id)
    es = cate.essay_set.order_by('-created_time')
    categories = Category.objects.all()
    context = {'cate': cate, 'es': es, 'categories': categories}
    return render(request, 'essay/cate.html', context)


def tag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    es = tag.essay_set.order_by('-created_time')
    categories = Category.objects.all()
    context = {'tag': tag, 'es': es, 'categories': categories}
    return render(request, 'essay/tag.html', context)


def detail(request, article_id):
    """文章详情页"""
    es = Essay.objects.get(id=article_id)  # 查询指定ID的文章
    content = markdown.markdown(es.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',  # 语法高亮拓展
        'markdown.extensions.toc'  # 自动生成目录
    ])
    categories = Category.objects.all()
    hot = Essay.objects.all().order_by('?')[:10]  # 内容下面的您可能感兴趣的文章，随机推荐
    tags = es.tags.all()
    previous_blog = Essay.objects.filter(
        created_time__gt=es.created_time, cate=es.cate.id).first()
    netx_blog = Essay.objects.filter(
        created_time__lt=es.created_time, cate=es.cate.id).last()
    cate_name = es.cate.name
    es.views = es.views + 1
    es.save()
    return render(request, 'essay/detail.html', locals())


@login_required
def new_essay(request, cate_id):
    """在特定分类下新发表文章"""
    cate = Category.objects.get(id=cate_id)
    categories = Category.objects.all()
    if request.method != 'POST':
        form = EssayForm()
    else:
        form = EssayForm(data=request.POST)
        if form.is_valid():
            new_essay = form.save(commit=False)
            new_essay.cate = cate
            new_essay.user = request.user
            new_essay.save()
            return redirect('essay:detail', article_id=new_essay.id)
    context = {'cate': cate, 'form': form, 'categories': categories}
    return render(request, 'essay/new_essay.html', context)


@login_required
def edit_essay(request, essay_id):
    """编辑已发表的文章"""
    es = Essay.objects.get(id=essay_id)
    cate = es.cate
    categories = Category.objects.all()  # 导航栏

    if es.user != request.user:
        return render(
            request,
            'essay/denied.html',
            {'categories': categories, 'cate': cate})

    if request.method != 'POST':
        # 初次请求，使用当前条目填充
        form = EssayForm(instance=es)
    else:
        # 对POST提交的数据进行处理
        form = EssayForm(instance=es, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('essay:detail', article_id=essay_id)
    context = {'es': es, 'cate': cate, 'form': form, 'categories': categories}
    return render(request, 'essay/edit_essay.html', context)


@login_required
def search(request):
    """搜索全站获取需要的文章"""
    search = request.GET.get('search')
    # 用 Q对象 进行联合搜索
    es_list = Essay.objects.filter(
        Q(title__icontains=search) |
        Q(content__icontains=search)
    )
    # 分页
    paginator = Paginator(es_list, 5)
    page = request.GET.get('page')
    es = paginator.get_page(page)
    categories = Category.objects.all()  # 导航栏
    articles = Essay.objects.all()[:8]

    context = {
        'es': es,
        'search': search,
        'categories': categories,
        'articles': articles}
    return render(request, 'essay/search.html', context)


@login_required
def user_essay(request, user_id):
    """展示用户文章"""
    user = User.objects.get(id=user_id)
    es = Essay.objects.filter(user=user)
    categories = Category.objects.all()  # 导航栏

    context = {'user': user, 'es': es, 'categories': categories}
    return render(request, 'essay/user_essay.html', context)
