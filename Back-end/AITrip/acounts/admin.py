from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin interface
    """
    # Fields to display in the user list
    list_display = ('email', 'username', 'get_full_name', 'is_active', 'is_staff', 'create_time', 'update_time')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'create_time', 'update_time')
    search_fields = ('email', 'username', 'first_name', 'middle_name', 'last_name')
    ordering = ('-create_time',)
    
    # Fields for user detail/edit form
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'middle_name', 'last_name')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'create_time', 'update_time'),
        }),
    )
    
    # Fields for add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'middle_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('create_time', 'update_time', 'last_login')
    
    # Override to make email the primary identifier
    def get_full_name(self, obj):
        """Display full name in admin list"""
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
