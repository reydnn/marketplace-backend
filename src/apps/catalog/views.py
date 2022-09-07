from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from apps.catalog.models import Product, Category
from apps.catalog.serializers import ProductSerializer, CategorySerializer


class CategoryViewSet(ModelViewSet):
    """
    ViewSet, который возвращает список всех категорий
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = ...


class ProductsViewSet(ModelViewSet):
    """
    ViewSet, который возращает список всех товаров
    """

    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    # permission_classes = ...
    filter_backends = [SearchFilter]
    search_fields = ["name"]
