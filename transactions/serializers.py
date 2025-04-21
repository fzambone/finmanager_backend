from rest_framework import serializers
from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    Uses PrimaryKeyRelatedField for account and category fields,
    with querysets filtered dynamically to the user's family group.
    """

    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
    )

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Transaction
        fields = [
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
        ]
        read_only_fields = ["family_group"]

    def __init__(self, *args, **kwargs):
        """
        Override __init__ method to dynamically filter the family group queryset
        for 'account' and 'category' based on the request user's group.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        request = self.context.get("request", None)

        if request and hasattr(request, "user") and request.user.is_authenticated:
            user_group = request.user.family_groups.first()

            if user_group:
                account_queryset = Account.objects.filter(family_group=user_group)
                self.fields["account"].queryset = account_queryset
                category_queryset = Category.objects.filter(family_group=user_group)
                self.fields["category"].queryset = category_queryset
            else:
                self.fields["account"].queryset = Account.objects.none()
                self.fields["category"].queryset = Category.objects.none()

    def validate(self, data):
        """
        Validate the 'account' and 'category' fields based on the request user's group.
        :param data:
        :return:
        """
        account = data.get("account")
        category = data.get("category")

        if account and category and account.family_group != category.family_group:
            raise serializers.ValidationError(
                "Account and category must belong to the same family group."
            )

        return data
