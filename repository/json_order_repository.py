import os
import json
from .i_order_repository import IOrderRepository

class JsonOrderRepository(IOrderRepository):
    """
    Implementación CONCRETA del repositorio que usa archivos JSON.
    """
    def __init__(self, filepath="data/orders.json"):
        self.ORDERS_FILE = filepath
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        os.makedirs(os.path.dirname(self.ORDERS_FILE), exist_ok=True)

    def load_all(self):
        """Carga los pedidos desde el archivo JSON."""
        if os.path.exists(self.ORDERS_FILE):
            with open(self.ORDERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_all(self, orders):
        """Guarda los pedidos en el archivo JSON."""
        self._ensure_data_dir()
        with open(self.ORDERS_FILE, "w", encoding="utf-8") as f:
            json.dump(orders, f, indent=4)