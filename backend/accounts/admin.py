from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email','username','is_staff','is_active',)
    list_filter = ('is_staff', 'is_active',)
    ordering = ('email',)
    search_fields = ('email', 'username',)
    fieldsets = ((None, {'fields': ('email', 'password',)}), ('Personal Info', {'fields': ('username',)}), ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}), ('Important Dates', {'fields': ('creation_timestamp',)}))
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'username', 'password', 'is_staff', 'is_active',)}))