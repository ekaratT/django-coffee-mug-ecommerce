from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    list_display = ['email', 'role', 'first_name', 'last_name', 'last_login', 'is_staff']
    ordering = ['-date_joined']
    filter_horizontal = []
    list_filter = []
    fieldsets = []

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)