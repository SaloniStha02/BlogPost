from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin

class AdminModify(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone_no', 'address', 'age']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_no', 'address', 'age')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_deleted')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(NewUser,AdminModify)
