from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, UserForm
from essay.models import Category, Essay


def register(request):
    """注册新用户。"""
    if request.method != 'POST':
        # 显示空的注册表单。
        form = RegisterForm()
    else:
        # 处理填写好的表单。
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录，再重定向到主页。
            login(request, new_user)
            return redirect('essay:index')

    categories = Category.objects.all()  # 导航栏
    # 显示空表单或指出表单无效。
    context = {'form': form, 'categories': categories}
    return render(request, 'registration/register.html', context)


@login_required
def my_account(request, user_id):
    """用户主页"""
    user = User.objects.get(id=user_id)
    es = Essay.objects.filter(user=user)
    categories = Category.objects.all()  # 导航栏

    context = {'user': user, 'es': es, 'categories': categories}
    return render(request, 'my_account/my_account.html', context)


@login_required
def edit_profile(request, user_id):
    """ 编辑用户信息 """
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        try:
            form = UserForm(request.POST, instance=user)
            user_profile_form = UserForm(request.POST, request.FILES, instance=user)  # 向表单填充默认数据
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect('users:my_account', user_id=user.id)
        except User.DoesNotExist:   # 这里发生错误说明user无数据
            form = UserForm(request.POST, instance=user)       # 填充默认数据 当前用户
            user_profile_form = UserForm(request.POST, request.FILES)  # 空表单，直接获取空表单的数据保存
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值添加进去，提交保存新的数据
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()
                return redirect('users:my_account', user_id=user.id)
    else:
        try:
            form = UserForm(instance=user)
            user_profile_form = UserForm(instance=user)
        except User.DoesNotExist:
            form = UserForm(instance=user)
            user_profile_form = UserForm()  # 显示空表单
    return render(request, 'my_account/edit_profile.html', locals())
