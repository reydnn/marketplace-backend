from django.conf import settings
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import CustomUser
from apps.orders.models import Order, OrderItem
from apps.catalog.models import Product, Category


class TestOrdersViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.time_pattern = settings.REST_FRAMEWORK.get("DATETIME_FORMAT")
        self.url = "/api/v1/orders/"
        self.user = CustomUser.objects.create(
            username="User",
            email="qwe@qwe.ru",
            is_staff=True,
            password="test2022",
        )
        self.category = Category.objects.create(name="Тест")
        self.product = Product.objects.create(
            category=self.category,
            name="Молоко",
            description="Сухое",
            price="100.00",
            stock=100,
        )
        self.product_post = Product.objects.create(
            category=self.category,
            name="Кефир",
            description="Кислый",
            price="100.00",
            stock=100,
        )
        self.order = Order.objects.create(
            user=self.user,
            delivery_address="Moscow",
            payment_method="Cash",
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=10,
        )
        self.client.force_authenticate(self.user)

    def test_order_get_list(self):
        exp_response = [
            {
                "id": self.order.id,
                "items": [
                    {
                        "id": self.order_item.id,
                        "product": self.product.id,
                        "quantity": self.order_item.quantity,
                        "subtotal": self.order_item.subtotal,
                    }
                ],
                "delivery_address": self.order.delivery_address,
                "payment_method": self.order.payment_method,
                "created": self.order.created.strftime(self.time_pattern),
                "updated": self.order.updated.strftime(self.time_pattern),
                "total_price": self.order.total_price,
            }
        ]

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], exp_response)
        self.assertEqual(len(response.json()["results"]), len(exp_response))

    def test_order_get_by_id(self):
        exp_response = {
            "id": self.order.id,
            "items": [
                {
                    "id": self.order_item.id,
                    "product": self.product.id,
                    "quantity": self.order_item.quantity,
                    "subtotal": self.order_item.subtotal,
                }
            ],
            "delivery_address": self.order.delivery_address,
            "payment_method": self.order.payment_method,
            "created": self.order.created.strftime(self.time_pattern),
            "updated": self.order.updated.strftime(self.time_pattern),
            "total_price": self.order.total_price,
        }

        response = self.client.get(path=f"{self.url}{self.order.id}/")
        print(f"{response=}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), exp_response)

    def test_order_post(self):
        data = {
            "items": [
                {
                    "product": self.product_post.id,
                    "quantity": 1,
                }
            ],
            "delivery_address": "Moscow",
            "payment_method": "Cash",
        }

        response = self.client.post(path=self.url, data=data, format="json")
        print(f"{response.json()=}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.json(), None)
