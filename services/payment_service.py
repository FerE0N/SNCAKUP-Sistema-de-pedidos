from abc import ABC, abstractmethod

class IPaymentService(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class MockPayPalSDK:
    """A mock 3rd party library."""
    def send_payment(self, total: float) -> str:
        print(f"PayPal SDK: Processing payment of ${total:.2f}")
        return "SUCCESS"

class PayPalAdapter(IPaymentService):
    """
    Adapter Pattern (Structural).
    Adapts MockPayPalSDK to IPaymentService.
    """
    def __init__(self):
        self.paypal = MockPayPalSDK()

    def process_payment(self, amount: float) -> bool:
        result = self.paypal.send_payment(amount)
        return result == "SUCCESS"
