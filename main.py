from flask import Flask, render_template, request, redirect, url_for, jsonify
import qrcode, os, uuid, json
from controller.controller_order import ControllerOrder
from controller.controller_product import ControllerProduct

app = Flask(__name__)

controller_order = ControllerOrder()
controller_product = ControllerProduct()

ORDERS_FILE = "data/orders.json"
current_order = None  # Mantiene el pedido actual en sesión temporal

# ------------------------
# UTILIDADES DE ARCHIVO
# ------------------------

def load_orders():
    """Carga los pedidos desde el archivo JSON."""
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_orders(orders):
    """Guarda los pedidos en el archivo JSON."""
    os.makedirs("data", exist_ok=True)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=4)

# ------------------------
# RUTAS PRINCIPALES
# ------------------------

@app.route('/')
def index():
    """
    Página principal: muestra el menú y permite crear una nueva orden.
    """
    products = controller_product.get_all_products()
    return render_template('screen_main.html', products=products)

# ------------------------
# CONFIRMAR ORDEN Y GENERAR QR
# ------------------------

@app.route("/confirm_order", methods=["POST"])
def confirm_order():
    """
    Recibe un pedido desde el frontend (JS) y genera su QR.
    """
    data = request.get_json()
    items = data.get("items", [])
    client_name = data.get("client_name", "Cliente desconocido")

    if not items:
        return jsonify({"success": False, "message": "Carrito vacío"})

    # Crear QR
    qr_id = str(uuid.uuid4())[:8]
    qr_text = f"Orden confirmada: {qr_id} | Cliente: {client_name}"
    qr_img = qrcode.make(qr_text)

    os.makedirs("static/qrcodes", exist_ok=True)
    qr_filename = f"{qr_id}.png"
    qr_path = os.path.join("static", "qrcodes", qr_filename)
    qr_img.save(qr_path)

    # Guardar la orden
    orders = load_orders()
    new_order = {
        "id": qr_id,
        "client_name": client_name,
        "items": items,
        "qr_filename": qr_filename
    }
    orders.append(new_order)
    save_orders(orders)

    return jsonify({"success": True, "qr_filename": qr_filename})

# ------------------------
# HISTORIAL DE ÓRDENES (JSON)
# ------------------------

@app.route("/get_orders", methods=["GET"])
def get_orders():
    """
    Devuelve todas las órdenes registradas en formato JSON.
    Este endpoint es consumido por el JS del historial.
    """
    orders = load_orders()
    return jsonify(orders)

# ------------------------
# MAIN ENTRY
# ------------------------

if __name__ == '__main__':
    if not os.path.exists('static/qrcodes'):
        os.makedirs('static/qrcodes')
    app.run(debug=True)
