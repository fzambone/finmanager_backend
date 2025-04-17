from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'family_group', 'parent_category', 'is_default')
    list_filter = ('family_group', 'parent_category', 'is_default')