from django.utils import timezone
from core.models import models, SoftDeleteModel
from categories.models import Category
from groups.models import FamilyGroup
from accounts.models import Account

class TransactionType(models.TextChoices):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSFER = 'transfer'

class Transaction(SoftDeleteModel):
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date_time = models.DateTimeField(default=timezone.now)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='transactions')
    payee_payer = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)
    family_group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payee_payer
