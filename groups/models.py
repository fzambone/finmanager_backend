from django.db import models
from django.contrib.auth.models import User
from core.models import SoftDeleteModel
from finmanager_backend import settings


class FamilyGroup(SoftDeleteModel):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="family_groups")
    primary_currency = models.CharField(max_length=3, default="USD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
