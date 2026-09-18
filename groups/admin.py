from django.contrib import admin
from .models import Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'mentor', 'province', 'city', 'status', 'created_at')
    list_filter = ('status', 'province')
    search_fields = ('name', 'mentor__phone_number')
