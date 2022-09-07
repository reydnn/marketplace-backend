from rest_framework.serializers import ModelSerializer

from apps.catalog.models import Product, Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "description",
            "price",
            "stock",
            "created",
            "updated",
            "available",
        ]
