from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


class FamilyGroupQuerysetMixin:
    """
    A mixin for ViewSets to handle common logic related to Family Groups:
    - Requires authentication.
    - Filters querysets to the user's group.
    - Assigns the user's group on creation.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters the queryset to objects belonging to the user's family group.
        Assumes the inheriting ViewSet has a 'queryset' or 'model' attribute defined.
        :return:
        """
        queryset = super().get_queryset()
        user = self.request.user

        if not user.is_authenticated:
            return queryset.none()

        user_groups = user.family_groups.all()
        if not user_groups.exists():
            return queryset.none()

        user_group = user_groups.first()
        return queryset.filter(family_group=user_group)

    def perform_create(self, serializer):
        """
        Assigns the user's family group automatically on creation.
        :param serializer:
        :return:
        """
        user = self.request.user
        user_groups = user.family_groups.all()

        if not user_groups.exists():
            raise serializers.ValidationError("User does not belong to a family group.")

        user_group = user_groups.first()
        serializer.save(family_group=user_group)
