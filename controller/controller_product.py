# controller/controller_product.py
from model.product import Product

class ControllerProduct:
    def __init__(self):
        self.products = [
            Product("Taco al pastor", 25.0),
            Product("Torta de milanesa", 35.0),
            Product("Agua de horchata", 15.0)
        ]

    def get_all_products(self):
        return self.products
