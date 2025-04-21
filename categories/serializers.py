from rest_framework import serializers
from categories.models import Category


class SimpleCategorySerializer(serializers.ModelSerializer):
    """
    A simplified serializer for the Category model, used for nested representation
    to avoid infinite recursion. Includes only essential fields.
    """

    class Meta:
        model = Category
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model, including nested representation for
    parent and sub-categories using the SimpleCategorySerializer.
    """

    parent_category = SimpleCategorySerializer(read_only=True)
    sub_categories = SimpleCategorySerializer(many=True, read_only=True)
    parent_category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="parent_category",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "family_group",
            "parent_category",
            "parent_category_id",
            "sub_categories",
            "is_default",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["family_group"]

    def __init__(self, *args, **kwargs):
        """
        Override __init__ method to dynamically filter the queryset for
        'parent_category_id' based on the request user's group.
        """
        super().__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and hasattr(request, "user") and request.user.is_authenticated:
            user_group = request.user.family_groups.first()
            if user_group:
                parent_queryset = Category.objects.filter(family_group=user_group)
                self.fields["parent_category_id"].queryset = parent_queryset
            else:
                self.fields["parent_category_id"].queryset = Category.objects.none()
