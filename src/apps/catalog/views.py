from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from apps.catalog.models import Product, Category
from apps.catalog.permissions import CategoryPermissions, ProductsPermissions
from apps.catalog.serializers import ProductSerializer, CategorySerializer


class CategoryViewSet(ModelViewSet):
    """
    ViewSet для CRUD операций с моделью Category
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermissions]


class ProductsViewSet(ModelViewSet):
    """
    ViewSet для CRUD операций с моделью Products
    """

    serializer_class = ProductSerializer
    permission_classes = [ProductsPermissions]
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        return Product.objects.select_related("category").filter(category=self.kwargs.get("categories_pk"))
