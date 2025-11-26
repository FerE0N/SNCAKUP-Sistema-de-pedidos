from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os

# Importamos las abstracciones y las clases
from controller.controller_product import ControllerProduct
from controller.controller_order import ControllerOrder
from controller.auth_controller import AuthController
from repository.mongo_order_repository import MongoOrderRepository
from services.payment_service import PayPalAdapter
from services.observer import KitchenObserver, EmailObserver
from services.strategies import NoDiscount, StudentDiscount, HappyHourDiscount
from services.mongo_connection import MongoConnection
from services.logger_service import LoggerService

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY" # Needed for session

# --- Configuración de Inyección de Dependencias (DI) ---

# 0. Database Connection
# Initialized automatically by Singleton access in Repositories

# 1. Repository
order_repository = MongoOrderRepository()

# 2. Payment Service (Adapter)
payment_service = PayPalAdapter()

# 3. Controllers
controller_product = ControllerProduct()
controller_order = ControllerOrder(order_repository, payment_service)
auth_controller = AuthController()

# 4. Observers
kitchen_observer = KitchenObserver()
email_observer = EmailObserver()
controller_order.subject.attach(kitchen_observer)
controller_order.subject.attach(email_observer)

# 5. Logger
logger = LoggerService()

# ---------------------------------------------------------

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_controller.login(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Credenciales inválidas")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_controller.register(username, password):
            return render_template('register.html', success="Usuario creado exitosamente.")
        else:
            return render_template('register.html', error="El usuario ya existe.")
    return render_template('register.html')

@app.route('/logout')
def logout():
    username = session.get('username')
    if username:
        logger.info(f"User logged out: {username}", user=username)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """
    Página principal: muestra el menú.
    """
    products = controller_product.get_all_products()
    return render_template('screen_main.html', products=products, username=session['username'])

@app.route("/confirm_order", methods=["POST"])
@login_required
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
    try:
        result = controller_order.create_order(client_name, items, total_amount)
        return jsonify(result)
    except Exception as e:
        logger.error(f"ERROR in confirm_order: {e}", user=client_name, details={"error": str(e)})
        print(f"ERROR in confirm_order: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Error interno: {str(e)}"}), 500

@app.route("/get_orders", methods=["GET"])
@login_required
def get_orders():
    try:
        current_user = session.get('username')
        orders = controller_order.get_orders_by_user(current_user)
        return jsonify(orders)
    except Exception as e:
        logger.error(f"ERROR in get_orders: {e}", user=session.get('username'), details={"error": str(e)})
        print(f"ERROR in get_orders: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Error al cargar historial: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)