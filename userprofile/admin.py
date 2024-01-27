from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['avatar', 'nickname', 'description', 'user_social']


admin.site.register(CustomUser, CustomUserAdmin)
