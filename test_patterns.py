from model.factories import ProductFactory
from model.decorators import ExtraCheese, LargeSize
from services.qr_manager import QRCodeManager
from services.strategies import StudentDiscount, HappyHourDiscount
from services.observer import OrderSubject, KitchenObserver
from services.payment_service import PayPalAdapter

def test_patterns():
    print("--- TEST DE PATRONES DE DISEÑO ---\n")

    # 1. Factory Method (Creational)
    print("1. Factory Method:")
    taco = ProductFactory.create_product("food", "Taco", 20.0)
    print(f"   Creado: {taco.get_description()} - ${taco.get_price()}")
    assert taco.get_description() == "Comida: Taco"

    # 2. Decorator (Structural)
    print("\n2. Decorator:")
    taco_con_queso = ExtraCheese(taco)
    print(f"   Decorado: {taco_con_queso.get_description()} - ${taco_con_queso.get_price()}")
    assert taco_con_queso.get_price() == 35.0  # 20 + 15

    # 3. Singleton (Creational)
    print("\n3. Singleton (QRCodeManager):")
    m1 = QRCodeManager()
    m2 = QRCodeManager()
    print(f"   m1 es m2? {m1 is m2}")
    assert m1 is m2

    # 4. Strategy (Behavioral)
    print("\n4. Strategy (Descuentos):")
    price = 100.0
    strategy = StudentDiscount()
    discounted = strategy.apply_discount(price)
    print(f"   Precio original: {price}, Con descuento estudiante: {discounted}")
    assert discounted == 90.0

    # 5. Observer (Behavioral)
    print("\n5. Observer:")
    subject = OrderSubject()
    observer = KitchenObserver()
    subject.attach(observer)
    print("   Notificando orden...")
    subject.new_order("TEST-123") # Should print to console

    # 6. Adapter (Structural)
    print("\n6. Adapter (Payment):")
    adapter = PayPalAdapter()
    result = adapter.process_payment(50.0)
    print(f"   Pago procesado: {result}")
    assert result is True

    print("\n--- TODOS LOS TESTS PASARON EXITOSAMENTE ---")

if __name__ == "__main__":
    test_patterns()
