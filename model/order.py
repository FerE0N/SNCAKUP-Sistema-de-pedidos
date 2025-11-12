import uuid

class Order:
    def __init__(self, client_name):
        self.id = str(uuid.uuid4())[:8]
        self.client_name = client_name
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product_name):
        self.products = [p for p in self.products if p.name != product_name]

    def total(self):
        return sum(p.price for p in self.products)
