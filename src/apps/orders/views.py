from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.orders.models import Order
from apps.orders.serializaers import OrderSerializer


class OrderViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):

    queryset = Order.objects.select_related("user")
    serializer_class = OrderSerializer
