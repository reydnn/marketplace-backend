from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.catalog.views import CategoryViewSet, ProductsViewSet

router = DefaultRouter()

router.register("products", ProductsViewSet)
router.register("categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
