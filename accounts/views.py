from rest_framework.viewsets import ModelViewSet
from core.views_mixins import FamilyGroupQuerysetMixin
from .models import Account
from .serializers import AccountSerializer


class AccountViewSet(FamilyGroupQuerysetMixin, ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited
    from users in the family group.
    Uses FamilyGroupQuerysetMixin for permissions and queryset filtering.
    """

    serializer_class = AccountSerializer
    queryset = Account.objects.all()
