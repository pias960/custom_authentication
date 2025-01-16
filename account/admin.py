from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('name', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    readonly_fields = ('date_joined', 'update_time')  # Keep password editable for admin changes
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'is_student', 'is_teacher', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('date_joined', 'update_time')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active', 'is_student', 'is_teacher'),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_student', 'is_teacher')
    search_fields = ('name', 'email')
    ordering = ('name', 'email')
    filter_horizontal = ('groups', 'user_permissions')  # Enable user-friendly filtering

# Register the User model with the custom admin class
@admin.register(User)
class UserAdmin(CustomUserAdmin):
    pass
