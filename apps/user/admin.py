from django.contrib import admin
from django.utils.html import format_html

from apps.user.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from utils.admin.mixins import DateListFilterMixin


@admin.register(User)
class MyUserAdmin(UserAdmin, DateListFilterMixin):
    list_display = ('render_avatar', 'email', 'user_name', 'first_name', 'last_name', 'created_at', 'last_login', 'is_active', 'is_staff')
    list_filter = ('first_name', 'last_name')
    readonly_fields = ('render_avatar', 'created_at', 'last_login')
    search_fields = ('email', 'user_name', 'first_name', 'last_name')
    ordering = ('-created_at',)
    fieldsets = (
        (_('basic'), {'fields': (('avatar', 'render_avatar'), 'email', 'user_name', 'first_name', 'last_name')}),
        (_('Personal'), {'fields': ('about',)}),
        (_('Important dates'), {'fields': ('created_at', 'last_login')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        ('Avatar', {
            'classes': ('wide',),
            'fields': ('avatar',),
        }),
        ('Required Fields', {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', 'password1', 'password2'),
        }),
        ('Optional Fields', {
            'classes': ('wide',),
            'fields': ('about', 'is_active', 'is_staff'),
        }),
    )

    def render_avatar(self, obj):
        return format_html(
            f'<img src="{obj.avatar.url}" width="50px" style="max-height:50px;" />'
        )
    render_avatar.short_description = 'Avatar'

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        super().delete_queryset(request, queryset)
