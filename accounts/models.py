from core.models import models, SoftDeleteModel
from groups.models import FamilyGroup


class AccountType(models.TextChoices):
    CHECKING = "checking", "Checking"
    SAVINGS = "savings", "Savings"


class Account(SoftDeleteModel):
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    currency = models.CharField(max_length=3, default="USD")
    starting_balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00
    )
    family_group = models.ForeignKey(
        FamilyGroup, on_delete=models.CASCADE, related_name="accounts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
