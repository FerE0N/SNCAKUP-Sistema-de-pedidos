from model.order import Order
import qrcode
import os

class ControllerOrder:
    def __init__(self):
        self.orders = []

    def create_order(self, client_name):
        order = Order(client_name)
        self.orders.append(order)
        return order

    def generate_qr(self, order_id):
        data = f"Order ID: {order_id} - Confirmed"
        img = qrcode.make(data)
        path = f"static/qrcodes/{order_id}.png"
        os.makedirs("static/qrcodes", exist_ok=True)
        img.save(path)
        return path
