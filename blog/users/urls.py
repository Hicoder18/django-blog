"""为应用程序users定义URL模式"""

from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # 包含默认的身份验证URL
    path('', include('django.contrib.auth.urls')),

    # 注册页面
    path('register/', views.register, name='register'),

    # 用户主页
    path('<int:user_id>/', views.my_account, name='my_account'),

    # 用户修改资料
    path('edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
]
