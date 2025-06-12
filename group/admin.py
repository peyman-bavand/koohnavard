from django.contrib import admin
from.models import Group, GroupMember, GroupImageGallery
from django.contrib.admin import ModelAdmin
# Register your models here.

admin.site.register(GroupMember)
admin.site.register(GroupImageGallery)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'leader', 'created_at')
    search_fields = (
        'name',
        'leader__username',  # برای جستجو بر اساس نام کاربری لیدر'(فارین کی سرچ)
        )