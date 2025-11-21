from abc import ABC, abstractmethod

class Product(ABC):
    """
    Abstract Base Class for all products.
    Demonstrates Abstraction and is the base for Polymorphism.
    """
    def __init__(self, name, price):
        self._name = name
        self._price = price

    @abstractmethod
    def get_price(self) -> float:
        """Returns the price of the product."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Returns the description of the product."""
        pass

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

class Food(Product):
    """Concrete implementation of Product for Food items."""
    def get_price(self) -> float:
        return self._price

    def get_description(self) -> str:
        return f"Comida: {self._name}"

class Drink(Product):
    """Concrete implementation of Product for Drink items."""
    def get_price(self) -> float:
        return self._price

    def get_description(self) -> str:
        return f"Bebida: {self._name}"