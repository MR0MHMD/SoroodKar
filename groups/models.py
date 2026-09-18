from django.db import models
from django.conf import settings


class Group(models.Model):
    STATUS_CHOICES = (
        ('pending_subscription', 'منتظر اشتراک'),
        ('pending_profile', 'منتظر تکمیل اطلاعات'),
        ('pending_mentor', 'منتظر منتور'),
    )

    # مدیر گروه (لیدر)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='managed_groups',
        verbose_name='مدیر گروه'
    )

    # منتور گروه (اختیاری - بعداً تخصیص داده میشه)
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mentored_groups',
        verbose_name='منتور'
    )

    name = models.CharField(max_length=255, verbose_name='نام گروه')
    province = models.CharField(max_length=100, verbose_name='استان')
    city = models.CharField(max_length=100, verbose_name='شهر')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending_subscription',
                              verbose_name='وضعیت')
    is_active = models.BooleanField('فعال باشد؟', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
