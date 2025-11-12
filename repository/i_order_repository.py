from abc import ABC, abstractmethod

class IOrderRepository(ABC):
    """
    Define la 'interfaz' (el contrato) para cualquier repositorio de órdenes.
    No le importa si es JSON, SQL, o una API; solo define QUÉ se puede hacer.
    """

    @abstractmethod
    def load_all(self):
        """Carga todas las órdenes."""
        pass

    @abstractmethod
    def save_all(self, orders):
        """Guarda la lista completa de órdenes."""
        pass