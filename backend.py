from abc import ABC, abstractmethod
from typing import List, Dict, Optional

# ==========================================
# INTERFACES Y CLASES ABSTRACTAS (DIP y OCP)
# ==========================================

class MetodoPago(ABC):
    """
    [Principio OCP] Abierto a extensión, cerrado a modificación.
    Si mañana necesitas agregar ApplePay, solo creas una nueva clase
    que herede de MetodoPago sin tocar el GestorPedidos.
    """
    @abstractmethod
    def procesarPago(self, monto: float) -> bool:
        pass

class PagoTarjeta(MetodoPago):
    def procesarPago(self, monto: float) -> bool:
        print(f"💳 Procesando pago de ${monto:.2f} mediante Tarjeta de Crédito...")
        return True # Simulación exitosa

class PagoPaypal(MetodoPago):
    def procesarPago(self, monto: float) -> bool:
        print(f"🅿️ Procesando pago de ${monto:.2f} mediante PayPal...")
        return True # Simulación exitosa

class SistemaNotificacion:
    def enviarMensaje(self, email: str, msj: str):
        print(f"📧 [Notificación a {email}]: {msj}")


# ==========================================
# JERARQUÍA DE USUARIOS (Herencia y Factory)
# ==========================================

class Usuario(ABC):
    def __init__(self, id_usuario: int, nombre: str, email: str):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email

    @abstractmethod
    def obtenerDatos(self) -> str:
        pass

class Cliente(Usuario):
    def __init__(self, id_usuario: int, nombre: str, email: str, direccionEntrega: str):
        super().__init__(id_usuario, nombre, email)
        self.direccionEntrega = direccionEntrega

    def obtenerDatos(self) -> str:
        return f"Cliente: {self.nombre} | Email: {self.email} | Dirección: {self.direccionEntrega}"

    def realizarPedido(self):
        print(f"🛍️ El cliente {self.nombre} está iniciando un pedido.")

class Restaurante(Usuario):
    def __init__(self, id_usuario: int, nombre: str, email: str, menu: List[Dict]):
        super().__init__(id_usuario, nombre, email)
        self.menu = menu # Ejemplo: [{'item': 'Pizza', 'precio': 15.0}]

    def obtenerDatos(self) -> str:
        return f"Restaurante: {self.nombre} | Items en menú: {len(self.menu)}"

    def prepararPedido(self, pedido: 'Pedido'):
        print(f"👨‍🍳 Restaurante {self.nombre} está preparando el pedido #{pedido.id}.")
        pedido.actualizarEstado("En Preparación")

class Repartidor(Usuario):
    def __init__(self, id_usuario: int, nombre: str, email: str, vehiculo: str):
        super().__init__(id_usuario, nombre, email)
        self.vehiculo = vehiculo
        self.disponible = True

    def obtenerDatos(self) -> str:
        estado = "Disponible" if self.disponible else "Ocupado"
        return f"Repartidor: {self.nombre} | Vehículo: {self.vehiculo} | Estado: {estado}"

    def actualizarUbicacion(self):
        print(f"📍 Ubicación de {self.nombre} actualizada.")

    def completarEntrega(self, pedido: 'Pedido'):
        pedido.actualizarEstado("Entregado")
        self.disponible = True
        print(f"✅ Repartidor {self.nombre} ha entregado el pedido #{pedido.id}.")


# ==========================================
# PATRÓN CREACIONAL: FACTORY METHOD
# ==========================================
class UsuarioFactory:
    """
    [Factory Method] Encapsula la lógica de instanciación de los distintos tipos de usuarios.
    Mantiene el código cliente limpio de constructores complejos.
    """
    @staticmethod
    def crear_usuario(tipo: str, **kwargs) -> Usuario:
        if tipo == "Cliente":
            return Cliente(kwargs['id'], kwargs['nombre'], kwargs['email'], kwargs['direccion'])
        elif tipo == "Restaurante":
            return Restaurante(kwargs['id'], kwargs['nombre'], kwargs['email'], kwargs.get('menu', []))
        elif tipo == "Repartidor":
            return Repartidor(kwargs['id'], kwargs['nombre'], kwargs['email'], kwargs['vehiculo'])
        raise ValueError("Tipo de usuario no soportado.")


# ==========================================
# CLASES CORE Y LÓGICA DE NEGOCIO
# ==========================================

class Pedido:
    def __init__(self, id_pedido: int, cliente: Cliente, restaurante: Restaurante, items_comprados: List[Dict]):
        self.id = id_pedido
        self.estado = "Creado"
        self.total = 0.0
        self.cliente = cliente
        self.restaurante = restaurante
        self.repartidor: Optional[Repartidor] = None
        self.items_comprados = items_comprados # Lista de items seleccionados del menú

    def calcularTotal(self) -> float:
        """[Principio SRP] El pedido es responsable de calcular su propio total."""
        self.total = sum(item['precio'] for item in self.items_comprados)
        return self.total

    def actualizarEstado(self, nuevoEstado: str):
        self.estado = nuevoEstado
        print(f"🔄 Pedido #{self.id} cambió de estado a: '{self.estado}'")


class GestorPedidos:
    """
    [Patrón Singleton] Garantiza una única instancia del gestor de pedidos.
    [Principio DIP] Depende de la abstracción MetodoPago, no de implementaciones concretas.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GestorPedidos, cls).__new__(cls)
            # Inicialización de atributos agregados
            cls._instancia.procesadorPago = None 
            cls._instancia.notificador = SistemaNotificacion()
        return cls._instancia

    def configurar_metodo_pago(self, metodo: MetodoPago):
        """Inyección de dependencias para el procesador de pagos."""
        self.procesadorPago = metodo

    def confirmarPedido(self, pedido: Pedido, cliente: Cliente):
        if not self.procesadorPago:
            raise ValueError("Error: Método de pago no configurado.")
        
        # Polimorfismo en acción
        pago_exitoso = self.procesadorPago.procesarPago(pedido.total)
        
        if pago_exitoso:
            pedido.actualizarEstado("Confirmado")
            self.notificador.enviarMensaje(cliente.email, f"Tu pedido #{pedido.id} ha sido confirmado y pagado exitosamente.")
        else:
            pedido.actualizarEstado("Pago Fallido")


# ==========================================
# SCRIPT DE PRUEBA: 10 FUNCIONALIDADES CRUD
# ==========================================
if __name__ == "__main__":
    print("--- INICIANDO SISTEMA DE DELIVERY ---")
    
    # 1. Crear clientes, restaurantes y repartidores (Usando Factory)
    cliente1 = UsuarioFactory.crear_usuario("Cliente", id=1, nombre="Ana", email="ana@mail.com", direccion="Av. Siempre Viva 123")
    
    menu_italiano = [{'item': 'Pizza Margarita', 'precio': 12.5}, {'item': 'Lasagna', 'precio': 15.0}]
    restaurante1 = UsuarioFactory.crear_usuario("Restaurante", id=101, nombre="Luigi's", email="contacto@luigis.com", menu=menu_italiano)
    
    repartidor1 = UsuarioFactory.crear_usuario("Repartidor", id=201, nombre="Carlos", email="carlos@delivery.com", vehiculo="Moto Honda")
    
    print("\n--- VISUALIZACIÓN DE ENTIDADES ---")
    print(cliente1.obtenerDatos())
    print(restaurante1.obtenerDatos())
    print(repartidor1.obtenerDatos())

    # 2. Modificar el estado de disponibilidad de un repartidor
    # Simulamos que Carlos terminó su turno temporalmente
    repartidor1.disponible = False
    print(f"\nDisponibilidad de {repartidor1.nombre} actualizada a: {repartidor1.disponible}")
    # Lo volvemos a poner disponible para el flujo principal
    repartidor1.disponible = True

    # 3. Visualizar el menú de un restaurante
    print(f"\n--- MENÚ DE {restaurante1.nombre.upper()} ---")
    for idx, item in enumerate(restaurante1.menu, 1):
        print(f"{idx}. {item['item']} - ${item['precio']}")

    # 4. Crear un nuevo pedido vinculando cliente y restaurante
    cliente1.realizarPedido()
    items_pedidos = [restaurante1.menu[0], restaurante1.menu[1]] # Compra una pizza y una lasagna
    pedido1 = Pedido(id_pedido=1001, cliente=cliente1, restaurante=restaurante1, items_comprados=items_pedidos)

    # 5. Calcular el total del pedido
    total_a_pagar = pedido1.calcularTotal()
    print(f"Total calculado del pedido #{pedido1.id}: ${total_a_pagar:.2f}")

    # 6. Asignar automáticamente un repartidor disponible
    # En un sistema real esto buscaría en una lista (CRUD), aquí iteramos una simulada
    lista_repartidores = [repartidor1]
    for rep in lista_repartidores:
        if rep.disponible:
            pedido1.repartidor = rep
            rep.disponible = False # Pasa a estar ocupado
            print(f"Asignación Automática: Repartidor {rep.nombre} asignado al pedido #{pedido1.id}.")
            break

    # 7. Procesar el pago utilizando polimorfismo
    gestor = GestorPedidos() # Instancia Singleton
    # Inyectamos el método de pago concreto (puede cambiarse en tiempo de ejecución por PagoPaypal())
    gestor.configurar_metodo_pago(PagoTarjeta()) 

    # 8 y 9. Confirmar pedido (envía notificaciones y cambia estados internamente)
    print("\n--- PROCESAMIENTO Y CONFIRMACIÓN ---")
    gestor.confirmarPedido(pedido1, cliente1)

    # Flujo de preparación y entrega (cambios de estado dinámicos)
    restaurante1.prepararPedido(pedido1)
    
    pedido1.actualizarEstado("En Camino")
    repartidor1.actualizarUbicacion()
    
    repartidor1.completarEntrega(pedido1)

    # 10. Visualizar el resumen completo del pedido finalizado
    print("\n--- RESUMEN FINAL DEL PEDIDO ---")
    print(f"ID Pedido: {pedido1.id}")
    print(f"Estado Final: {pedido1.estado}")
    print(f"Cliente: {pedido1.cliente.nombre} ({pedido1.cliente.direccionEntrega})")
    print(f"Restaurante: {pedido1.restaurante.nombre}")
    print(f"Repartidor Asignado: {pedido1.repartidor.nombre}")
    print("Detalle de Items:")
    for item in pedido1.items_comprados:
         print(f" - {item['item']}: ${item['precio']}")
    print(f"TOTAL PAGADO: ${pedido1.total:.2f}")