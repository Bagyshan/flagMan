from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'is_company', 'is_verified_email', 'verification_code', 'is_superuser', 'registered_at', 'updated_at')
    list_filter = ('is_company', 'is_verified_email', 'is_superuser')
    search_fields = ('email',)
    readonly_fields = (
        'verification_code',
        'verification_code_created_at',
        'password_reset_code',
        'password_reset_code_created_at',
        'new_email_verification_code',
        'new_email_verification_code_created_at'
    )