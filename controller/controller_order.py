# controller/controller_order.py
from model.order import Order

class ControllerOrder:
    def __init__(self):
        self.orders = []

    def create_order(self, client_name):
        order = Order(client_name)
        self.orders.append(order)
        return order

    def get_all_orders(self):
        return self.orders
