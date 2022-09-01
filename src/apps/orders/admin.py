from django.contrib import admin

from apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ["product", "quantity", "subtotal"]
    readonly_fields = ["subtotal"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display: list[str] = ["user", "delivery_address", "payment_method", "created", "updated", "total_price"]
    list_filter: list[str] = ["payment_method", "created", "updated"]
    inlines = [OrderItemInline]
