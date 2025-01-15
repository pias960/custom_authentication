from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('name', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    readonly_fields = ('password', 'date_joined', 'update_time')
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'is_student', 'is_teacher')}),
        ('Important Dates', {'fields': ('date_joined', 'update_time')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active', 'is_student', 'is_teacher'),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('name', 'email')
    ordering = ('name', 'email')
    filter_horizontal = ()  # Removed 'groups' and 'user_permissions'

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)
