from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('شماره موبایل باید وارد شود')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('سوپریوزر باید is_staff=True باشد.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('سوپریوزر باید is_superuser=True باشد.')

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # نقش‌های کاربری - فقط دو نقش اصلی
    ROLE_CHOICES = (
        ('group_manager', 'مدیر گروه'),  # لیدر گروه سرود
        ('mentor', 'منتور'),  # منتور و راهنمای گروه
    )

    phone_number = models.CharField(max_length=15, unique=True, verbose_name='شماره موبایل')
    username = models.CharField(max_length=150, unique=True, blank=True, null=True, verbose_name='نام کاربری')
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='نام و نام خانوادگی')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True, verbose_name='نقش')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return f"{self.phone_number} - {self.full_name or 'بدون نام'}"
