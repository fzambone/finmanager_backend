from rest_framework import viewsets
from core.views_mixins import FamilyGroupQuerysetMixin
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer


class TransactionViewSet(FamilyGroupQuerysetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited within the
    family group that the user is a member of.
    Uses FamilyGroupQuerysetMixin for permissions and queryset filtering.
    """

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
