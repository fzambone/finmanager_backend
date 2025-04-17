from django.contrib import admin
from .models import FamilyGroup


@admin.register(FamilyGroup)
class FamilyGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'primary_currency')
    list_display_links = ('id', 'name')
    list_filter = ('primary_currency',)