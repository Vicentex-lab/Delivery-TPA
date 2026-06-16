from abc import ABC, abstractmethod

# ==========================================
# INTERFACES Y CLASES ABSTRACTAS (DIP y OCP)
# ==========================================

class MetodoPago(ABC):
    """
    [Principio OCP] Abierto a extension pero cerrado a modificacion
    En caso que queramos agregar cualquier metodo de pago extra (Appleplay, crypto, etc)
    Unicamente creamos esa nueva clase que herede de metodo pago
    sin tocar el GestorPedidos. Así no modificamos código ya funcional.
    """
    @abstractmethod
    def procesarPago(self, monto: float) -> bool:
        pass

class PagoTarjeta(MetodoPago):
    def procesarPago(self, monto: float) -> bool:
        print(f"Procesando pago de ${monto:.2f} mediante Tarjeta de Crédito...")
        return True 

class PagoPaypal(MetodoPago):
    def procesarPago(self, monto: float) -> bool:
        print(f"Procesando pago de ${monto:.2f} mediante PayPal...")
        return True 
    
class MetodoPagoDecorator(MetodoPago):
    """Clase base para los decoradores de pago."""
    def __init__(self, metodo_base: MetodoPago):
        self._metodo_base = metodo_base

    def procesarPago(self, monto: float) -> bool:
        return self._metodo_base.procesarPago(monto)

class CargoServicioDecorator(MetodoPagoDecorator):
    """Decorador concreto que añade un 5% de cargo por uso de la app."""
    def procesarPago(self, monto: float) -> bool:
        monto_con_cargo = monto * 1.05
        print(f"Aplicando 5% de cargo por servicio. Nuevo monto a procesar: ${monto_con_cargo:.2f}")
        return super().procesarPago(monto_con_cargo)
    
class SistemaNotificacion:
    def enviarMensaje(self, email: str, msj: str):
        print(f"[Notificación a {email}]: {msj}")
