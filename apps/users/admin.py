from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email','username','role','is_active']
    list_filter = ['role','is_active']
    fieldsets = UserAdmin.fieldsets + (('Role',{'fields': ('role',)}),)
    
    
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone']        