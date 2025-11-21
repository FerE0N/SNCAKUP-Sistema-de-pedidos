from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

# Importamos las abstracciones y las clases
from controller.controller_product import ControllerProduct
from controller.controller_order import ControllerOrder
from repository.json_order_repository import JsonOrderRepository
from services.payment_service import PayPalAdapter
from services.observer import KitchenObserver, EmailObserver
from services.strategies import NoDiscount, StudentDiscount, HappyHourDiscount

app = Flask(__name__)

# --- Configuración de Inyección de Dependencias (DI) ---

# 1. Repository
order_repository = JsonOrderRepository("data/orders.json")

# 2. Payment Service (Adapter)
payment_service = PayPalAdapter()

# 3. Controllers
controller_product = ControllerProduct()
controller_order = ControllerOrder(order_repository, payment_service)

# 4. Observers
kitchen_observer = KitchenObserver()
email_observer = EmailObserver()
controller_order.subject.attach(kitchen_observer)
controller_order.subject.attach(email_observer)

# ---------------------------------------------------------

@app.route('/')
def index():
    """
    Página principal: muestra el menú.
    """
    products = controller_product.get_all_products()
    return render_template('screen_main.html', products=products)

@app.route("/confirm_order", methods=["POST"])
def confirm_order():
    data = request.get_json()
    items = data.get("items", [])
    client_name = data.get("client_name", "Cliente desconocido")
    discount_type = data.get("discount_type", "none")

    if not items:
        return jsonify({"success": False, "message": "Carrito vacío"})

    # Calculate total
    try:
        total_amount = sum(float(item.get('price', 0)) for item in items)
    except ValueError:
        return jsonify({"success": False, "message": "Error en precios de items"})

    # Set Strategy
    if discount_type == "student":
        controller_order.set_discount_strategy(StudentDiscount())
    elif discount_type == "happy_hour":
        controller_order.set_discount_strategy(HappyHourDiscount())
    else:
        controller_order.set_discount_strategy(NoDiscount())

    # Create Order
    result = controller_order.create_order(client_name, items, total_amount)
    
    return jsonify(result)

@app.route("/get_orders", methods=["GET"])
def get_orders():
    orders = order_repository.load_all()
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)