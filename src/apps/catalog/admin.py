from django.contrib import admin

from apps.catalog.models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display: list[str] = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display: list[str] = ["name", "price", "stock", "available", "created", "updated"]
    list_filter: list[str] = ["created"]
