from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('full_name', 'phone')}),
    )
    list_display = ('username', 'email', 'full_name', 'phone', 'is_staff')
    search_fields = ('username', 'email', 'full_name', 'phone')
    ordering = ('-date_joined',)
