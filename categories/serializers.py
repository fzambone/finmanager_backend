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
            "created_at",
            "updated_at",
        ]
