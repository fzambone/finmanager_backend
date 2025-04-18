from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "account_type", "currency", "family_group")
    list_filter = ("account_type", "currency", "family_group")
