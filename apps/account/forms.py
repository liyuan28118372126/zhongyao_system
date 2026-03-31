"""Account forms."""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class SignUpForm(UserCreationForm):
    """Sign up form."""
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    password1 = forms.CharField(
        label="密码",
        strip=False,
        widget=forms.PasswordInput,
        help_text="密码至少8个字符，不能太常见，不能全是数字",
    )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput,
        strip=False,
        help_text="请再次输入密码以确认",
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': '用户名',
            'email': '邮箱',
        }
        help_texts = {
            'username': '请输入用户名',
            'email': '请输入有效的邮箱地址',
        }


class LoginForm(AuthenticationForm):
    """Login form."""
    pass


class UserProfileForm(forms.ModelForm):
    """User profile form."""
    class Meta:
        model = UserProfile
        fields = ('avatar', 'bio', 'phone_number')
        labels = {
            'avatar': '头像',
            'bio': '个人简介',
            'phone_number': '联系电话',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
