from rest_framework import serializers
from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for the Account model.

    Translates Account mode instances to JSON and validates incoming data.
    """

    class Meta:
        model = Account

        fields = [
            "id",
            "name",
            "account_type",
            "currency",
            "starting_balance",
            "family_group",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "family_group",
        ]
