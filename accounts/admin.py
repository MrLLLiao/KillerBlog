from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('扩展字段', {'fields': ('avatar', 'bio')}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('扩展字段', {'fields': ('email', 'avatar', 'bio')}),
    )
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
