from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "transaction_type",
        "amount",
        "date_time",
        "account",
        "category",
        "payee_payer",
        "description",
        "is_recurring",
        "family_group",
        "created_at",
        "updated_at",
    )
