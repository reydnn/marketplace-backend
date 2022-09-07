from django.urls import path, include

from rest_framework_nested import routers

from apps.catalog.views import CategoryViewSet, ProductsViewSet

categories_router = routers.SimpleRouter()
categories_router.register("categories", CategoryViewSet)

product_router = routers.NestedSimpleRouter(categories_router, "categories", lookup="categories")
product_router.register("products", ProductsViewSet, basename="categories-products")


urlpatterns = [
    path("", include(categories_router.urls)),
    path("", include(product_router.urls)),
]
