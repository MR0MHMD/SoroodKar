from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('groups:create_group')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # لاگین خودکار بعد از ثبت‌نام
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد. لطفاً اطلاعات گروه خود را وارد کنید.')
            return redirect('groups:create_group')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('groups:create_group')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, 'ورود با موفقیت انجام شد.')
            return redirect('groups:create_group')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'از حساب خود خارج شدید.')
    return redirect('accounts:login')