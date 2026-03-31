"""Account views."""

from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, UserProfileForm
from apps.sales.models import Supply, Demand


def signup(request):
    """Sign up view."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('medicine:index')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


def user_login(request):
    """Login view."""
    # 检查用户是否已经登录，如果已登录则重定向到首页
    if request.user.is_authenticated:
        return redirect('medicine:index')
    
    next_url = request.POST.get('next') or request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url or 'medicine:index')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form, 'next': next_url})


def user_logout(request):
    """Logout view."""
    logout(request)
    return redirect('account:login')


@login_required
def my_profile(request):
    """User profile view."""
    user = request.user
    try:
        profile = user.userprofile
    except:
        profile = None
    
    # 获取用户发布的供应和需求信息
    supplies = Supply.objects.filter(user=user)
    demands = Demand.objects.filter(user=user)
    
    return render(request, 'account/profile.html', {
        'user': user,
        'profile': profile,
        'supplies': supplies,
        'demands': demands
    })


@login_required
def edit_profile(request):
    """Edit user profile view."""
    user = request.user
    try:
        profile = user.userprofile
    except:
        from .models import UserProfile
        profile = UserProfile(user=user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'account/edit_profile.html', {
        'form': form,
        'user': user
    })
