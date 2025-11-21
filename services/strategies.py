from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    """
    Strategy Pattern (Behavioral).
    Defines a family of algorithms (discounts).
    """
    @abstractmethod
    def apply_discount(self, amount: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply_discount(self, amount: float) -> float:
        return amount

class StudentDiscount(DiscountStrategy):
    def apply_discount(self, amount: float) -> float:
        return amount * 0.90  # 10% off

class HappyHourDiscount(DiscountStrategy):
    def apply_discount(self, amount: float) -> float:
        return amount * 0.80  # 20% off
