from repository.i_order_repository import IOrderRepository
from services.qr_manager import QRCodeManager
from services.observer import OrderSubject
from services.strategies import DiscountStrategy, NoDiscount
from services.payment_service import IPaymentService
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

    def set_discount_strategy(self, strategy: DiscountStrategy):
        self.discount_strategy = strategy

    def create_order(self, client_name: str, items: list, total_amount: float):
        # 1. Apply Discount Strategy
        final_amount = self.discount_strategy.apply_discount(total_amount)
        
        # 2. Process Payment via Adapter
        if not self.payment_service.process_payment(final_amount):
            return {"success": False, "message": "Pago fallido"}

        # 3. Generate QR via Singleton Manager
        qr_id = str(uuid.uuid4())[:8]
        qr_text = f"Orden: {qr_id} | Cliente: {client_name} | Total: ${final_amount:.2f}"
        qr_filename = f"{qr_id}.png"
        self.qr_manager.generate_qr(qr_text, qr_filename)

        # 4. Save Order via Repository
        new_order = {
            "id": qr_id,
            "client_name": client_name,
            "items": items,
            "total": final_amount,
            "qr_filename": qr_filename
        }
        orders = self.repo.load_all()
        orders.append(new_order)
        self.repo.save_all(orders)

        # 5. Notify Observers (Kitchen, Email, etc.)
        self.subject.new_order(qr_id)

        return {"success": True, "qr_filename": qr_filename, "total": final_amount}
