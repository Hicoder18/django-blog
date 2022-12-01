"""定义文章应用essay的URL模式"""

from django.urls import path

from . import views

app_name = 'essay'
urlpatterns = [
    # 博客主页
    path('', views.index, name='index'),

    # 显示所有主题
    path('category', views.category, name='category'),

    # 特定文章分类页面
    path('category/<int:cate_id>/', views.cate, name='cate'),

    # 文章标签
    path('tag', views.tag, name='tag'),
    path('tag/<int:tag_id>', views.tag, name='tag'),

    # 文章详情页
    path('detail-<int:article_id>.html', views.detail, name='detail'),

    # 新发表文章
    path('new_essay', views.new_essay, name='new_essay'),
    path('new_essay/<int:cate_id>/', views.new_essay, name='new_essay'),

    # 修改文章
    path('edit_essay', views.edit_essay, name='edit_essay'),
    path('edit_essay/<int:essay_id>/', views.edit_essay, name='edit_essay'),

    # 搜索页面
    path('search/', views.search, name='search'),

    # 用户文章列表
    path('user_essay', views.user_essay, name='user_essay'),
    path('user_essay/<int:user_id>/', views.user_essay, name='user_essay'),
]
