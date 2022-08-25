from django.db import models


class Category(models.Model):
    """Категория"""

    name = models.CharField(
        max_length=200,
        db_index=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Продукт"""

    category = models.ForeignKey(Category, related_name="products", on_delete=models.SET_NULL, null=True)
    name = models.CharField(
        max_length=200,
        db_index=True,
        null=False,
    )
    description = models.TextField(
        blank=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    stock = models.PositiveIntegerField()
    available = models.BooleanField(
        default=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name
