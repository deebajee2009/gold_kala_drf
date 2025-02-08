from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserWallet

class UserAdmin(BaseUserAdmin):
    list_display = ('user_id', 'username', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    search_fields = ('username',)
    ordering = ('user_id',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(UserWallet)
