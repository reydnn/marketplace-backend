from datetime import datetime

from django.conf import settings
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import CustomUser
from apps.catalog.models import Product, Category


class TestCategoryViewSet(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.category = Category.objects.create(name="Тест")
        self.category_url = "/api/v1/catalog/categories/"
        self.user = CustomUser.objects.create(
            username="User",
            email="qwe@qwe.ru",
            is_staff=True,
            password="test2022",
        )
        self.client.force_authenticate(self.user)

    def test_category_get_list(self):
        categories = list(Category.objects.all().values())
        response = self.client.get(self.category_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], categories)
        self.assertEqual(len(response.json()["results"]), len(categories))

    def test_category_get_by_id(self):
        exp_response = {
            "id": self.category.id,
            "name": self.category.name,
        }

        response = self.client.get(f"{self.category_url}{self.category.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), exp_response)

    def test_category_post(self):
        exp_name = "Овощи"

        input_data = {
            "name": exp_name,
        }

        response = self.client.post(self.category_url, data=input_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["name"], exp_name)

    def test_category_put(self):
        new_name = "Фрукты"

        input_data = {
            "name": new_name,
        }

        exp_response = {"id": self.category.id, "name": new_name}

        response = self.client.put(
            path=f"{self.category_url}{self.category.id}/",
            data=input_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), exp_response)

    def test_category_patch(self):
        new_name = "Хлеб"

        input_data = {
            "name": new_name,
        }

        exp_response = {"id": self.category.id, "name": new_name}

        response = self.client.patch(
            path=f"{self.category_url}{self.category.id}/",
            data=input_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), exp_response)

    def test_category_delete(self):
        response = self.client.delete(f"{self.category_url}{self.category.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestProductsViewSet(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.category = Category.objects.create(name="Тест")
        self.time_pattern = settings.REST_FRAMEWORK.get("DATETIME_FORMAT")
        self.product = Product.objects.create(
            category=self.category,
            name="Молоко",
            description="Сухое",
            price="100.00",
            stock=10,
        )
        self.products_url = f"/api/v1/catalog/categories/{self.category.id}/products/"

        self.user = CustomUser.objects.create(
            username="User",
            email="qwe@qwe.ru",
            is_staff=True,
            password="test2022",
        )
        self.client.force_authenticate(self.user)

    def test_products_get_list(self):
        products = list(Product.objects.all().values())

        for product in products:
            product["category"] = product["category_id"]
            product["created"] = product["created"].strftime(self.time_pattern)
            product["updated"] = product["updated"].strftime(self.time_pattern)
            product["price"] = str(product["price"])
            product["available"] = bool(product["stock"])
            del product["category_id"]

        response = self.client.get(self.products_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], products)
        self.assertEqual(len(response.json()["results"]), len(products))

    def test_products_get_by_id(self):

        exp_response = {
            "id": self.product.id,
            "name": self.product.name,
            "category": self.product.category.id,
            "description": self.product.description,
            "price": self.product.price,
            "stock": self.product.stock,
            "created": self.product.created.strftime(self.time_pattern),
            "updated": self.product.updated.strftime(self.time_pattern),
            "available": self.product.available,
        }

        response = self.client.get(f"{self.products_url}{self.product.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), exp_response)

    def test_products_post(self):

        input_data = {
            "name": "test",
            "category": self.category.id,
            "description": "test",
            "price": "100.40",
            "stock": 5,
        }

        response = self.client.post(self.products_url, data=input_data, format="json")
        exp_response = {
            **input_data,
            "created": datetime.now().strftime(self.time_pattern),
            "updated": datetime.now().strftime(self.time_pattern),
            "available": True,
        }
        response_data = dict(response.json())
        del response_data["id"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data, exp_response)

    def test_products_put(self):
        input_data = {
            "name": "test",
            "category": self.category.id,
            "description": "test",
            "price": "100.40",
            "stock": 5,
        }

        exp_response = {
            **input_data,
            "id": self.product.id,
            "created": self.product.created.strftime(self.time_pattern),
            "updated": datetime.now().strftime(self.time_pattern),
            "available": True,
        }

        response = self.client.put(
            path=f"{self.products_url}{self.product.id}/",
            data=input_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), exp_response)

    def test_products_patch(self):
        new_name = "Qwerty"

        input_data = {
            "name": new_name,
        }

        response = self.client.patch(
            path=f"{self.products_url}{self.product.id}/",
            data=input_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], new_name)

    def test_products_delete(self):
        response = self.client.delete(f"{self.products_url}{self.product.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
