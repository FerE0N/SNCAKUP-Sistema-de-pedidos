from .product import Product

class ProductDecorator(Product):
    """
    Decorator Pattern (Structural).
    Wraps a Product to add functionality dynamically.
    """
    def __init__(self, product: Product):
        # We don't call super().__init__ because we delegate to the wrapped product
        self._product = product

    def get_price(self) -> float:
        return self._product.get_price()

    def get_description(self) -> str:
        return self._product.get_description()

class ExtraCheese(ProductDecorator):
    def get_price(self) -> float:
        return self._product.get_price() + 15.0

    def get_description(self) -> str:
        return f"{self._product.get_description()} + Queso Extra"

class LargeSize(ProductDecorator):
    def get_price(self) -> float:
        return self._product.get_price() * 1.20

    def get_description(self) -> str:
        return f"{self._product.get_description()} (Grande)"
