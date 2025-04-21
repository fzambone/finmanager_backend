from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

router = DefaultRouter()
router.register(r"transactions", views.TransactionViewSet, basename="transactions")

app_name = "transactions"

urlpatterns = [
    path("", include(router.urls)),
]
