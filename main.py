from flask import Flask, render_template, request, redirect, url_for, jsonify
import qrcode, os, uuid
# Importamos las abstracciones y las clases
from controller.controller_product import ControllerProduct
from repository.i_order_repository import IOrderRepository
from repository.json_order_repository import JsonOrderRepository

# --- Configuración de Inyección de Dependencias (DI) ---
# En una app grande, esto lo haría un framework de DI.
# Aquí lo hacemos manualmente al inicio.

app = Flask(__name__)

# 1. Creamos las implementaciones concretas
controller_product = ControllerProduct()
# Le decimos al repositorio dónde guardar los datos
order_repository: IOrderRepository = JsonOrderRepository("data/orders.json")

# NOTA: No necesitamos 'controller_order' porque la lógica
# de crear órdenes ahora está ligada a la persistencia (el repo).
# ---------------------------------------------------------


@app.route('/')
def index():
    """
    Página principal: muestra el menú.
    """
    products = controller_product.get_all_products()
    return render_template('screen_main.html', products=products)

# ------------------------
# CONFIRMAR ORDEN Y GENERAR QR
# ------------------------

@app.route("/confirm_order", methods=["POST"])
def confirm_order():
    """
    Recibe un pedido y lo guarda usando el repositorio.
    """
    data = request.get_json()
    items = data.get("items", [])
    client_name = data.get("client_name", "Cliente desconocido")

    if not items:
        return jsonify({"success": False, "message": "Carrito vacío"})

    # --- Lógica de QR (Sigue siendo responsabilidad de la ruta) ---
    qr_id = str(uuid.uuid4())[:8]
    qr_text = f"Orden confirmada: {qr_id} | Cliente: {client_name}"
    qr_img = qrcode.make(qr_text)
    os.makedirs("static/qrcodes", exist_ok=True)
    qr_filename = f"{qr_id}.png"
    qr_path = os.path.join("static", "qrcodes", qr_filename)
    qr_img.save(qr_path)
    
    # --- Lógica de Persistencia (Abstraída) ---
    # Ya no sabemos NADA sobre JSON. Solo usamos el repositorio.
    orders = order_repository.load_all()
    
    new_order = {
        "id": qr_id,
        "client_name": client_name,
        "items": items,
        "qr_filename": qr_filename
    }
    orders.append(new_order)
    
    # Le pedimos al repositorio que guarde.
    order_repository.save_all(orders)

    return jsonify({"success": True, "qr_filename": qr_filename})

# ------------------------
# HISTORIAL DE ÓRDENES (JSON)
# ------------------------

@app.route("/get_orders", methods=["GET"])
def get_orders():
    """
    Devuelve todas las órdenes desde el repositorio.
    """
    # Ya no llamamos a una función local, usamos el repositorio.
    orders = order_repository.load_all()
    return jsonify(orders)

# ------------------------
# MAIN ENTRY
# ------------------------

if __name__ == '__main__':
    if not os.path.exists('static/qrcodes'):
        os.makedirs('static/qrcodes')
    app.run(debug=True)