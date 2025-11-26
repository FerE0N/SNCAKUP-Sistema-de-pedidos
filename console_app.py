import os
import sys
from time import sleep

# Add current directory to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Dependencies
from controller.controller_product import ControllerProduct
from controller.controller_order import ControllerOrder
from controller.auth_controller import AuthController
from repository.mongo_order_repository import MongoOrderRepository
from services.payment_service import PayPalAdapter
from services.observer import KitchenObserver, EmailObserver
from services.strategies import NoDiscount, StudentDiscount, HappyHourDiscount

# --- Initialization (Same as main.py) ---
order_repository = MongoOrderRepository()
payment_service = PayPalAdapter()

controller_product = ControllerProduct()
controller_order = ControllerOrder(order_repository, payment_service)
auth_controller = AuthController()

# Observers
kitchen_observer = KitchenObserver()
email_observer = EmailObserver()
controller_order.subject.attach(kitchen_observer)
controller_order.subject.attach(email_observer)

# --- CLI Helpers ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("="*40)
    print("      🍿 SNACKUP CONSOLE v1.0 🍿      ")
    print("="*40)

def pause():
    input("\nPresiona Enter para continuar...")

# --- Flows ---

def login_flow():
    print_header()
    print("--- INICIAR SESIÓN ---")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    
    if auth_controller.login(username, password):
        print(f"\n✅ ¡Bienvenido, {username}!")
        return username
    else:
        print("\n❌ Credenciales inválidas.")
        pause()
        return None

def register_flow():
    print_header()
    print("--- REGISTRO ---")
    username = input("Nuevo Usuario: ")
    password = input("Contraseña: ")
    
    if auth_controller.register(username, password):
        print(f"\n✅ Usuario {username} creado exitosamente.")
    else:
        print("\n❌ El usuario ya existe.")
    pause()

def create_order_flow(username):
    print_header()
    print(f"Usuario: {username}")
    print("--- CREAR ORDEN ---\n")
    
    # 1. Show Menu
    products = controller_product.get_all_products()
    print("MENÚ DISPONIBLE:")
    for i, p in enumerate(products):
        print(f"{i+1}. {p.name} - ${p.price:.2f} ({p.category})")
    
    items = []
    while True:
        choice = input("\nSelecciona el número del producto (o 'f' para finalizar): ")
        if choice.lower() == 'f':
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(products):
                qty = int(input(f"Cantidad de '{products[idx].name}': "))
                if qty > 0:
                    # Add to items list (format expected by controller)
                    # Note: Controller expects dicts with 'price' key for total calc in main.py logic
                    # But here we can calculate total ourselves or pass objects.
                    # Let's stick to the dict format used in main.py for consistency
                    item = {
                        "name": products[idx].name,
                        "price": products[idx].price,
                        "quantity": qty
                    }
                    # Add multiple times or just once with qty? 
                    # main.py logic: sum(float(item.get('price', 0)) for item in items)
                    # It seems main.py expects a flat list of items where each item is one unit.
                    # Let's replicate that for compatibility.
                    for _ in range(qty):
                        items.append(item)
                    print(f"✅ {qty}x {products[idx].name} agregado(s).")
            else:
                print("❌ Opción inválida.")
        except ValueError:
            print("❌ Entrada inválida.")

    if not items:
        print("\n⚠️ Carrito vacío. Cancelando orden.")
        pause()
        return

    # 2. Select Discount
    print("\n--- DESCUENTO ---")
    print("1. Ninguno")
    print("2. Estudiante (10%)")
    print("3. Happy Hour (20%)")
    disc_choice = input("Selecciona descuento (1-3): ")
    
    if disc_choice == '2':
        controller_order.set_discount_strategy(StudentDiscount())
    elif disc_choice == '3':
        controller_order.set_discount_strategy(HappyHourDiscount())
    else:
        controller_order.set_discount_strategy(NoDiscount())

    # 3. Calculate Total
    total_amount = sum(float(item['price']) for item in items)
    
    # 4. Confirm
    print(f"\nTotal estimado: ${total_amount:.2f}")
    confirm = input("¿Confirmar orden? (s/n): ")
    
    if confirm.lower() == 's':
        result = controller_order.create_order(username, items, total_amount)
        if result['success']:
            print("\n✅ ORDEN CREADA EXITOSAMENTE!")
            print(f"Total Final: ${result['total']:.2f}")
            print(f"QR ID: {result['qr_base64'][:20]}...") # Truncate base64
        else:
            print(f"\n❌ Error: {result['message']}")
    else:
        print("\nOrden cancelada.")
    
    pause()

def view_history_flow(username):
    print_header()
    print(f"--- HISTORIAL DE PEDIDOS ({username}) ---\n")
    
    orders = controller_order.get_orders_by_user(username)
    if not orders:
        print("No hay pedidos registrados.")
    else:
        for order in orders:
            print(f"🆔 {order.get('id', 'N/A')}")
            print(f"👤 Cliente: {order.get('client_name', 'N/A')}")
            print(f"💰 Total: ${order.get('total', 0):.2f}")
            print(f"🛒 Items: {len(order.get('items', []))}")
            print("-" * 20)
    
    pause()

# --- Main Loop ---

def main():
    current_user = None
    
    while True:
        print_header()
        if current_user:
            print(f"Usuario: {current_user}")
            print("1. 🍔 Ver Menú / Crear Orden")
            print("2. 📜 Ver Historial")
            print("3. 🚪 Cerrar Sesión")
            print("4. ❌ Salir")
            
            op = input("\nOpción: ")
            
            if op == '1':
                create_order_flow(current_user)
            elif op == '2':
                view_history_flow(current_user)
            elif op == '3':
                current_user = None
                print("\nSesión cerrada.")
                sleep(1)
            elif op == '4':
                print("\n¡Hasta luego!")
                break
            else:
                print("Opción inválida.")
                sleep(1)
        else:
            print("1. 🔐 Iniciar Sesión")
            print("2. 📝 Registrarse")
            print("3. ❌ Salir")
            
            op = input("\nOpción: ")
            
            if op == '1':
                current_user = login_flow()
            elif op == '2':
                register_flow()
            elif op == '3':
                print("\n¡Hasta luego!")
                break
            else:
                print("Opción inválida.")
                sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSaliendo...")
