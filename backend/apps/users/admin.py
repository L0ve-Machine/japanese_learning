from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProgress

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'native_language', 'is_premium', 'is_staff', 'created_at']
    list_filter = ['is_premium', 'native_language', 'is_staff']
    search_fields = ['email']
    ordering = ['-created_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('native_language', 'is_premium', 'subscription_end_date', 'stripe_customer_id')}),
    )

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'content_id', 'completed', 'score', 'completed_at']
    list_filter = ['completed', 'content_type']
    search_fields = ['user__email']