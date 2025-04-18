from core.models import models, SoftDeleteModel
from groups.models import FamilyGroup


class Category(SoftDeleteModel):
    name = models.CharField(max_length=100)
    family_group = models.ForeignKey(
        FamilyGroup, on_delete=models.CASCADE, related_name="categories"
    )
    parent_category = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sub_categories",
    )
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
