from django.db import models

from apps.users.models import CustomUser
from apps.products.models import Product


class Payment(models.TextChoices):
    """Оплата"""

    CASH = "Cash", "Наличные"
    CARD = "Card", "Банковская карта"


class Order(models.Model):
    """Заказы"""

    user = models.ForeignKey(
        CustomUser, verbose_name="Пользователь", on_delete=models.DO_NOTHING, null=False, blank=False
    )

    delivery_address = models.TextField(verbose_name="Адрес доставки", null=False, blank=False)

    payment_method = models.CharField(verbose_name="Способ оплаты", max_length=50, choices=Payment.choices)

    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.SET_NULL,
        null=True,
    )
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.id)
