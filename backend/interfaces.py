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
    
class SistemaNotificacion:
    def enviarMensaje(self, email: str, msj: str):
        print(f"[Notificación a {email}]: {msj}")
