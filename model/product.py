from abc import ABC, abstractmethod

class Product(ABC):
    """
    Abstract Base Class for all products.
    Demonstrates Abstraction and is the base for Polymorphism.
    """
    def __init__(self, name, price, image_url="https://placehold.co/400x300?text=Snack"):
        self._name = name
        self._price = price
        self._image_url = image_url

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

    @property
    def image_url(self):
        return self._image_url

class Food(Product):
    """Concrete implementation of Product for Food items."""
    def get_price(self) -> float:
        return self._price

    def get_description(self) -> str:
        return f"Comida: {self._name}"

    @property
    def category(self):
        return "Comida"

class Drink(Product):
    """Concrete implementation of Product for Drink items."""
    def get_price(self) -> float:
        return self._price

    def get_description(self) -> str:
        return f"Bebida: {self._name}"

    @property
    def category(self):
        return "Bebida"