from .product import Food, Drink, Product

class ProductFactory:
    """
    Factory Method Pattern (Creational).
    Centralizes the creation of Product objects.
    """
    @staticmethod
    def create_product(product_type, name, price, image_url=None):
        if image_url is None:
            # Default placeholders based on type
            if product_type.lower() == "food":
                image_url = "https://placehold.co/400x300?text=Food"
            elif product_type.lower() == "drink":
                image_url = "https://placehold.co/400x300?text=Drink"
            else:
                image_url = "https://placehold.co/400x300?text=Snack"

        if product_type.lower() == "food":
            return Food(name, price, image_url)
        elif product_type.lower() == "drink":
            return Drink(name, price, image_url)
        else:
            raise ValueError("Tipo de producto desconocido")
