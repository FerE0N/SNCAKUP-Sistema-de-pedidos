from model.product import Product

class ControllerProduct:
    def __init__(self):
        self.available_products = [
            Product("Sushi Roll", 120),
            Product("Onigiri", 45),
            Product("Ramen", 95),
            Product("Tempura", 80)
        ]

    def get_all_products(self):
        return self.available_products
