from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

router = DefaultRouter()

router.register(r"categories", views.CategoryViewSet, basename="categories")

app_name = "categories"

urlpatterns = [
    path("", include(router.urls)),
]
