from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админка для кастомной модели User"""

    fieldsets = UserAdmin.fieldsets + (
        ('Telegram', {'fields': ('telegram_chat_id',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Telegram', {'fields': ('telegram_chat_id',)}),
    )

    list_display = ('username', 'email', 'telegram_chat_id', 'is_staff')
    search_fields = ('username', 'email', 'telegram_chat_id')