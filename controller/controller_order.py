from repository.i_order_repository import IOrderRepository
from services.qr_manager import QRCodeManager
from services.observer import OrderSubject
from services.strategies import DiscountStrategy, NoDiscount
from services.payment_service import IPaymentService
from services.logger_service import LoggerService
import uuid

class ControllerOrder:
    """
    Controller for handling Order logic.
    Integrates Repository, Singleton, Observer, Strategy, and Adapter patterns.
    """
    def __init__(self, repo: IOrderRepository, payment_service: IPaymentService):
        self.repo = repo
        self.payment_service = payment_service
        self.qr_manager = QRCodeManager() # Singleton instance
        self.subject = OrderSubject()
        self.discount_strategy: DiscountStrategy = NoDiscount()
        self.logger = LoggerService()

    def set_discount_strategy(self, strategy: DiscountStrategy):
        self.discount_strategy = strategy

    def create_order(self, client_name: str, items: list, total_amount: float):
        # 1. Apply Discount Strategy
        final_amount = self.discount_strategy.apply_discount(total_amount)
        
        # 2. Process Payment via Adapter
        if not self.payment_service.process_payment(final_amount):
            self.logger.warning(f"Payment failed for order. Client: {client_name}", user=client_name)
            return {"success": False, "message": "Pago fallido"}

        # 3. Generate QR via Singleton Manager (Ephemeral Base64)
        qr_id = str(uuid.uuid4())[:8]
        qr_text = f"Orden: {qr_id} | Cliente: {client_name} | Total: ${final_amount:.2f}"
        qr_base64 = self.qr_manager.generate_qr_base64(qr_text)

        # 4. Save Order via Repository
        new_order = {
            "id": qr_id,
            "client_name": client_name,
            "items": items,
            "total": final_amount,
            "qr_base64": qr_base64 # Store Base64 string directly or just regenerate on fly? 
                                   # Storing it allows history to show it without regeneration.
        }
        orders = self.repo.load_all()
        orders.append(new_order)
        self.repo.save_all(orders)

        # 5. Notify Observers (Kitchen, Email, etc.)
        self.subject.new_order(qr_id)

        self.logger.info(f"Order created: #{qr_id} for {client_name} - Total: ${final_amount:.2f}", user=client_name)

        return {"success": True, "qr_base64": qr_base64, "total": final_amount}

    def get_all_orders(self):
        return self.repo.load_all()

    def get_orders_by_user(self, username: str):
        all_orders = self.repo.load_all()
        # Filter orders where 'client_name' matches the username
        return [order for order in all_orders if order.get('client_name') == username]
