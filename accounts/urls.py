from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

router = DefaultRouter()

router.register(r"accounts", views.AccountViewSet, basename="account")

app_name = "accounts"

urlpatterns = [
    path("", include(router.urls)),
]
