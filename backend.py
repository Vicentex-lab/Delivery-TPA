from abc import ABC, abstractmethod
from typing import List, Dict, Optional

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


# ==========================================
# JERARQUÍA DE USUARIOS (Herencia y Factory)
# ==========================================

class Usuario(ABC):
    def __init__(self, id_usuario: int, nombre: str, email: str, contraseña: str = "1234"): # Asigno contraseña por defecto "1234" temporalmente
        self.id = id_usuario
        self.nombre = nombre # se utiliza como nombre_usuario en la validación del login
        self.email = email
        self.contraseña = contraseña # nuevo atributo que almacena credencial de acceso
    
      
    @property #implementa un atributo de solo lectura que devuelve el tipo de rol como string
    @abstractmethod
    def rol(self) -> str:
        pass 

    @abstractmethod
    def obtenerDatos(self) -> str:
        pass

class Cliente(Usuario):
    def __init__(self, id_usuario: int, nombre: str, email: str, direccionEntrega: str, contraseña: str = "1234"):
        super().__init__(id_usuario, nombre, email, contraseña)
        self.direccionEntrega = direccionEntrega
        
    @property
    def rol(self) -> str:
        return "Cliente"

    def obtenerDatos(self) -> str:
        return f"Cliente: {self.nombre} | Email: {self.email} | Dirección: {self.direccionEntrega}"

    def realizarPedido(self):
        print(f"El cliente {self.nombre} está iniciando un pedido.")

class Restaurante(Usuario):
    def __init__(self, id_usuario: int, nombre: str, email: str, menu: List[Dict], contraseña: str = "1234"):
        super().__init__(id_usuario, nombre, email, contraseña)
        self.menu = menu # Ejemplo: [{'item': 'Completo', 'precio': 15.0}]
        
    @property
    def rol(self) -> str:
        return "Restaurante"    

    def obtenerDatos(self) -> str:
        return f"Restaurante: {self.nombre} | Items en menú: {len(self.menu)}"

    def prepararPedido(self, pedido: 'Pedido'):
        print(f"Restaurante {self.nombre} está preparando el pedido #{pedido.id}.")
        pedido.actualizarEstado("En Preparación")

class Repartidor(Usuario):
    def __init__(self, id_usuario: int, nombre: str, email: str, vehiculo: str, contraseña: str = "1234"):
        super().__init__(id_usuario, nombre, email, contraseña)
        self.vehiculo = vehiculo
        self.disponible = True
        
    @property
    def rol(self) -> str:
        return "Repartidor"

    def obtenerDatos(self) -> str:
        estado = "Disponible" if self.disponible else "Ocupado"
        return f"Repartidor: {self.nombre} | Vehículo: {self.vehiculo} | Estado: {estado}"

    def actualizarUbicacion(self):
        print(f" Ubicación de {self.nombre} actualizada.")

    def completarEntrega(self, pedido: 'Pedido'):
        pedido.actualizarEstado("Entregado")
        self.disponible = True
        print(f" Repartidor {self.nombre} ha entregado el pedido #{pedido.id}.")


# ==========================================
# PATRÓN CREACIONAL: FACTORY METHOD
# ==========================================
class UsuarioFactory:
    """
    Factory Method: Centraliza como se crean los usuarios. 
    Nos ahorra tener que armar objetos a mano en el flujo principal y mantiene el código limpio.
    """
    @staticmethod
    def crear_usuario(tipo: str, **kwargs) -> Usuario:
        if tipo == "Cliente":
            return Cliente(kwargs['id'], kwargs['nombre'], kwargs['email'], kwargs['direccion'], kwargs.get('contraseña', '1234')) #si no hay contraseña, asigna una genérica 1234
        elif tipo == "Restaurante":
            return Restaurante(kwargs['id'], kwargs['nombre'], kwargs['email'], kwargs.get('menu', []), kwargs.get('contraseña', '1234') )
        elif tipo == "Repartidor":
            return Repartidor(kwargs['id'], kwargs['nombre'], kwargs['email'], kwargs['vehiculo'], kwargs.get('contraseña', '1234'))
        raise ValueError("Tipo de usuario no soportado.")


# ==========================================
#LÓGICA DE NEGOCIO
# ==========================================

class Pedido:
    def __init__(self, id_pedido: int, cliente: Cliente, restaurante: Restaurante, items_comprados: List[Dict]):
        self.id = id_pedido
        self.estado = "Creado"
        self.total = 0.0
        self.cliente = cliente
        self.restaurante = restaurante
        self.repartidor: Optional[Repartidor] = None
        self.items_comprados = items_comprados # Lista de items seleccionados del menu

    def calcularTotal(self) -> float:
        """[Principio SRP] El pedido es responsable de calcular su propio total."""
        self.total = sum(item['precio'] for item in self.items_comprados)
        return self.total

    def actualizarEstado(self, nuevoEstado: str):
        self.estado = nuevoEstado
        print(f"Pedido #{self.id} cambió de estado a: '{self.estado}'")


class GestorPedidos:
    """
    [Patrón Singleton] Garantiza una única instancia del gestor de pedidos.
    [Principio DIP] Depende de la abstracción MetodoPago, no de implementaciones concretas.
    """
    _instancia = None
    
    #type hinting
    usuarios_registrados: List[Usuario]

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GestorPedidos, cls).__new__(cls)
            # Inicialización de atributos agregados
            cls._instancia.procesadorPago = None 
            cls._instancia.notificador = SistemaNotificacion()
            cls._instancia.usuarios_registrados = [] # Lista global simulada de persistencia de datos para el login
        return cls._instancia
    
    
    def registrar_usuario_sistema(self, usuario: Usuario):
        """Método auxiliar para que el backend reconozca a los usuarios creados"""
        self.usuarios_registrados.append(usuario)
        
        
    def validar_login(self, nombre_usuario: str, contraseña_ingresada: str) -> Optional[str]:
        """
        [Funcionalidad 1 - Backend] 
        Recibe las credenciales de la GUI, busca coincidencia y retorna el Rol si es exitoso.
        Retorna None si las credenciales son incorrectas.
        """
        for usuario in self.usuarios_registrados:
            if usuario.nombre == nombre_usuario and usuario.contraseña == contraseña_ingresada:
                print(f"[Login] Acceso concedido a {usuario.nombre} con el rol: {usuario.rol}")
                return usuario.rol  # Devuelve "Cliente", "Restaurante" o "Repartidor"
        
        print(f"[Login Fallido] Intento fallido de inicio de sesión para el usuario: {nombre_usuario}")
        return None

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
    cliente1 = UsuarioFactory.crear_usuario("Cliente", id=1, nombre="Antonia", email="antonia@mail.com", direccion="Manuel Rodriguez 1874")
    
    menu_italiano = [{'item': 'Pizza Margarita', 'precio': 12.5}, {'item': 'Palitos de ajo', 'precio': 5.0}]
    restaurante1 = UsuarioFactory.crear_usuario("Restaurante", id=101, nombre="Papa Johns", email="contacto@papajohns.com", menu=menu_italiano)
    
    repartidor1 = UsuarioFactory.crear_usuario("Repartidor", id=201, nombre="Esteban", email="esteban@delivery.com", vehiculo="Moto Suzuki")
    
    print("\n--- VISUALIZACIÓN DE ENTIDADES ---")
    print(cliente1.obtenerDatos())
    print(restaurante1.obtenerDatos())
    print(repartidor1.obtenerDatos())

    # 2. Modificar el estado de disponibilidad de un repartidor
    # Simulamos que Esteban terminó su turno temporalmente
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
    items_pedidos = [restaurante1.menu[0], restaurante1.menu[1]] # Ejemplo: compra una pizza y palitos de ajo
    pedido1 = Pedido(id_pedido=1001, cliente=cliente1, restaurante=restaurante1, items_comprados=items_pedidos)

    # 5. Calcular el total del pedido
    total_a_pagar = pedido1.calcularTotal()
    print(f"Total calculado del pedido #{pedido1.id}: ${total_a_pagar:.2f}")

    # 6. Asignar automáticamente un repartidor disponible
    lista_repartidores = [repartidor1]
    for rep in lista_repartidores:
        if rep.disponible:
            pedido1.repartidor = rep
            rep.disponible = False # Pasa a estar ocupado
            print(f"Asignación Automática: Repartidor {rep.nombre} asignado al pedido #{pedido1.id}.")
            break

    # 7. Procesar el pago utilizando polimorfismo
    gestor = GestorPedidos() # Instancia Singleton
    # Inyectamos el método de pago concreto 
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
    
    
    
    #Script func. 1
    """
    # === PRUEBA DE FUNCIONALIDAD 1: VALIDACIÓN DE LOGIN ===
    print("\n--- PROBANDO FUNCIONALIDAD 1: VALIDACIÓN DE LOGIN ---")
    gestor = GestorPedidos()
    
    # Asignamos una contraseña personalizada a un usuario de prueba
    cliente_login = UsuarioFactory.crear_usuario("Cliente", id=2, nombre="Vicente", email="v.cardenas@mail.com", direccion="Av. Central 123", contraseña="securePass123")
    
    # Registramos al usuario en el listado del gestor
    gestor.registrar_usuario_sistema(cliente_login)
    
    # Intento 1: Credenciales incorrectas
    resultado_fallido = gestor.validar_login("Vicente", "clave_erronea")
    print(f"Resultado esperado (None): {resultado_fallido}")
    
    # Intento 2: Credenciales correctas
    resultado_exitoso = gestor.validar_login("Vicente", "securePass123")
    print(f"Resultado esperado ('Cliente'): {resultado_exitoso}")
"""