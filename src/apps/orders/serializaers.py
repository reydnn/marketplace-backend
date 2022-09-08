from rest_framework import status
from rest_framework.serializers import HiddenField, ModelSerializer, CurrentUserDefault

from core.exceptions import ProductNotFoundError, ProductNotAvailableError
from apps.orders.models import Order, OrderItem
from apps.orders.exceptions import OrderBadRequest
from apps.orders.services.orders import OrderService


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "quantity",
            "subtotal",
        ]


class OrderSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "items",
            "delivery_address",
            "payment_method",
            "created",
            "updated",
            "total_price",
            "user",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        try:
            OrderService(items_data).execute()
        except (ProductNotFoundError, ProductNotAvailableError) as e:
            raise OrderBadRequest(detail=str(e), code=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
