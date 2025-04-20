from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Account
from . import serializers


class AccountViewSet(ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited
    from users in the family group.
    """

    serializer_class = serializers.AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(family_group__members=self.request.user)

    def perform_create(self, serializer):
        group = self.request.user.family_groups.first()

        if group is None:
            raise serializer.ValidationError("No family group found")

        serializer.save(family_group=group)
