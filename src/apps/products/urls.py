from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryViewSet, ProductsViewSet

router = DefaultRouter()

router.register("", ProductsViewSet)
router.register("categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
