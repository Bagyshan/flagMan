from django.contrib import admin
from .models import Favorite

@admin.register(Favorite)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', )