from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'full_name', 'role', 'is_active')
    search_fields = ('phone_number', 'full_name')
    ordering = ('phone_number',)

    # چون USERNAME_FIELD رو عوض کردیم، باید فیلدهای پیش‌فرض ادمین رو با مدل جدید هماهنگ کنیم
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('اطلاعات شخصی', {'fields': ('full_name', 'username', 'role')}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌های مهم', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'full_name', 'role'),
        }),
    )
