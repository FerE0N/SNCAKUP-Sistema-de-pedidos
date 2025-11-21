from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

class KitchenObserver(Observer):
    def update(self, message: str):
        print(f"[COCINA] Nueva orden recibida: {message}")

class EmailObserver(Observer):
    def update(self, message: str):
        print(f"[EMAIL] Enviando confirmación al cliente: {message}")

class OrderSubject(Subject):
    """
    Concrete Subject.
    Notifies observers when a new order is placed.
    """
    def new_order(self, order_id: str):
        self.notify(f"Orden #{order_id} creada exitosamente.")
