from .product import Food, Drink, Product

class ProductFactory:
    """
    Factory Method Pattern (Creational).
    Centralizes the creation of Product objects.
    """
    @staticmethod
    def create_product(product_type: str, name: str, price: float) -> Product:
        if product_type.lower() == "food":
            return Food(name, price)
        elif product_type.lower() == "drink":
            return Drink(name, price)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
