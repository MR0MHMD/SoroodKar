from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GroupCreateForm
from .models import Group


@login_required
def create_group_view(request):
    # اگه کاربر قبلاً گروه ساخته، بره به پنل
    if Group.objects.filter(manager=request.user).exists():
        messages.info(request, 'شما قبلاً یک گروه ساخته‌اید.')
        return redirect('groups:dashboard')  # بعداً این رو می‌سازیم

    if request.method == 'POST':
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.manager = request.user
            group.status = 'pending_subscription'
            group.save()
            messages.success(request, 'گروه شما با موفقیت ساخته شد. برای ادامه، اشتراک تهیه کنید.')
            return redirect('groups:dashboard')  # بعداً این رو می‌سازیم
    else:
        form = GroupCreateForm()

    return render(request, 'groups/create_group.html', {'form': form})