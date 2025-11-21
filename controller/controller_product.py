# controller/controller_product.py
from model.factories import ProductFactory

class ControllerProduct:
    def __init__(self):
        # Factory Method Pattern: Creating objects without specifying exact class
        self.products = [
            ProductFactory.create_product("food", "Taco al pastor", 25.0),
            ProductFactory.create_product("food", "Torta de milanesa", 35.0),
            ProductFactory.create_product("drink", "Agua de horchata", 15.0),
            ProductFactory.create_product("drink", "Refresco", 20.0)
        ]

    def get_all_products(self):
        return self.products
