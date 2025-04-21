from rest_framework import viewsets
from categories.models import Category
from categories.serializers import CategorySerializer
from core.views_mixins import FamilyGroupQuerysetMixin


class CategoryViewSet(FamilyGroupQuerysetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited within the
    family group that the user is a member of.
    Uses FamilyGroupQuerysetMixin for permissions and queryset filtering.
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
