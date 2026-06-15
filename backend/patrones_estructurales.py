from abc import ABC, abstractmethod
from typing import List, Dict

# ==========================================
# PATRÓN ESTRUCTURAL: DECORATOR
# ==========================================
class ComponenteCosto(ABC):
    @abstractmethod
    def obtener_costo(self) -> float:
        pass

class CostoBasePedido(ComponenteCosto):
    """Componente Concreto: Calcula el subtotal base de los platos."""
    def __init__(self, items: List[Dict]):
        self.items = items

    def obtener_costo(self) -> float:
        return sum(item['precio'] for item in self.items)

class CostoDecorator(ComponenteCosto):
    """Decorador Base"""
    def __init__(self, componente: ComponenteCosto):
        self._componente = componente

    def obtener_costo(self) -> float:
        return self._componente.obtener_costo()

class EnvioDecorator(CostoDecorator):
    """Decorador Concreto: Agrega la tarifa de envío."""
    def __init__(self, componente: ComponenteCosto, tarifa: float):
        super().__init__(componente)
        self.tarifa = tarifa

    def obtener_costo(self) -> float:
        return super().obtener_costo() + self.tarifa

class PropinaDecorator(CostoDecorator):
    """Decorador Concreto: Agrega la propina del repartidor."""
    def __init__(self, componente: ComponenteCosto, propina: float):
        super().__init__(componente)
        self.propina = propina

    def obtener_costo(self) -> float:
        return super().obtener_costo() + self.propina