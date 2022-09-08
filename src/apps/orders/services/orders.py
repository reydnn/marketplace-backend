from core.exceptions import ProductNotFoundError, ProductNotAvailableError
from apps.catalog.models import Product
from core.error_messages import PRODUCT_NOT_FOUND_ERROR, PRODUCT_NOT_AVAILABLE_ERROR


class OrderService:
    def __init__(self, items: list[dict]) -> None:
        self._items = items

    def execute(self) -> None:
        self._check_product_stock(self._items)

    def _check_product_stock(self, items: list[dict]) -> None:
        for item in items:
            try:
                product: Product = Product.objects.get(pk=item.get("product").id)
            except Product.DoesNotExist:
                raise ProductNotFoundError(PRODUCT_NOT_FOUND_ERROR.format(product.pk))

            self._update_product(product, item.get("quantity"))

    def _update_product(self, product: Product, item_qunatity: int):
        if product.available:
            new_stock = product.stock - item_qunatity
            Product.objects.filter(pk=product.id).update(stock=new_stock)
        else:
            raise ProductNotAvailableError(PRODUCT_NOT_AVAILABLE_ERROR.format(product.pk))
