from abc import ABC, abstractmethod

# ==========================================
# INTERFACES Y CLASES ABSTRACTAS (DIP y OCP)
# ==========================================


# PATRÓN DE COMPORTAMIENTO: STRATEGY (ESTRATEGIA)
# =========================================================================
# Componente: Estrategia Abstracta (Strategy Interface)
# Define la interfaz común para todos los algoritmos de pago soportados.
# Permite aplicar el principio Open/Closed (OCP).
# =========================================================================



class MetodoPago(ABC):
    """
    [Principio OCP] Abierto a extension pero cerrado a modificacion
    En caso que queramos agregar cualquier metodo de pago extra (Appleplay, crypto, etc)
    Unicamente creamos esa nueva clase que herede de metodo pago
    sin tocar el GestorPedidos. Así no modificamos código ya funcional.
    """
    @abstractmethod
    def procesarPago(self, monto: int) -> bool:
        pass

# =========================================================================
# Componente: Estrategia Concreta A (Concrete Strategy)
# Encapsula un algoritmo específico de pago mediante Tarjeta de Crédito.
# =========================================================================

class PagoTarjeta(MetodoPago):
    def procesarPago(self, monto: int) -> bool:
        print(f"Procesando pago de ${monto} mediante Tarjeta de Crédito...")
        return True 
# =========================================================================
# Componente: Estrategia Concreta B (Concrete Strategy)
# Encapsula un algoritmo específico de pago mediante PayPal.
# =========================================================================
class PagoPaypal(MetodoPago):
    def procesarPago(self, monto: int) -> bool:
        print(f"Procesando pago de ${monto} mediante PayPal...")
        return True 
    
class SistemaNotificacion:
    def enviarMensaje(self, email: str, msj: str):
        print(f"[Notificación a {email}]: {msj}")

class MetodoPagoDecorator(MetodoPago):
    """
    [Patrón Estructural: Decorator] 
    Clase base que envuelve a un MetodoPago utilizando composición.
    """
    def __init__(self, metodo_base: MetodoPago):
        self._metodo_base = metodo_base

    def procesarPago(self, monto: int) -> bool:
        return self._metodo_base.procesarPago(monto)

class CargoServicioDecorator(MetodoPagoDecorator):
    """
    [Patrón Estructural: Decorator] 
    Decorador concreto que añade dinámicamente un cargo por servicio del 5%.
    """
    def procesarPago(self, monto: int) -> bool:
        monto_con_cargo = int(monto * 1.05)
        print(f"[*] Patrón Decorator: Aplicando 5% de cargo por servicio app. Monto final: ${monto_con_cargo}")
        return super().procesarPago(monto_con_cargo)
