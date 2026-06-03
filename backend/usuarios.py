from abc import ABC, abstractmethod
from typing import List, Dict, Optional

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
        
    def actualizar_direccion(self, nueva_direccion: str):
        """[Funcionalidad 11] Permite cambiar la dirección de entrega desde la GUI"""
        self.direccionEntrega = nueva_direccion
        print(f"[*] Perfil Actualizado: Cliente {self.nombre} cambió su dirección a '{nueva_direccion}'.")
        
        
class Pedido:
    def __init__(self, id_pedido: int, cliente: Cliente, restaurante: 'Restaurante', items_comprados: List[Dict]):
        self.id = id_pedido
        self.estado = "Creado"
        self.subtotal = 0.0
        self.total = 0.0
        self.tarifa_envio = 0.0
        self.propina = 0.0
        self.cliente = cliente
        self.restaurante = restaurante
        self.repartidor: Optional[Repartidor] = None
        self.items_comprados = items_comprados 

    def calcularTotal(self, tarifa_envio: float = 0.0, propina: float = 0.0) -> float:
        """
        [Funcionalidad 13 - Cálculo Avanzado] 
        Aplica el Principio SRP calculando el subtotal base de los platos 
        e inyectando costos extras como el envío y la propina voluntaria.
        """
        self.subtotal = sum(item['precio'] for item in self.items_comprados)
        self.tarifa_envio = tarifa_envio
        self.propina = propina
        self.total = self.subtotal + self.tarifa_envio + self.propina
        return self.total

    def actualizarEstado(self, nuevo_estado: str):
        """
        [Funcionalidad 15 y 16 - Transición y Sincronización Automática]
        Cambia secuencialmente los estados del pedido: Creado -> Confirmado -> En Preparación -> En Camino -> Entregado.
        Sincroniza de forma automática la disponibilidad del repartidor según la fase.
        """
        self.estado = nuevo_estado
        print(f"[Pedido #{self.id}] Estado actualizado a: '{self.estado}'")
        
        # Sincronización automática del repartidor asociada al estado del pedido
        if self.repartidor:
            if nuevo_estado in ["Confirmado", "En Preparación", "En Camino"]:
                self.repartidor.disponible = False  # Ocupado mientras dure el flujo del delivery
            elif nuevo_estado in ["Entregado", "Cancelado"]:
                self.repartidor.disponible = True   # Vuelve a estar disponible inmediatamente al finalizar


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
        
        
    def modificar_item(self, nombre_plato: str, nuevo_precio: float):
        """[Funcionalidad 12] Busca un plato en el menú y actualiza su precio"""
        for item in self.menu:
            if item['item'].lower() == nombre_plato.lower():
                precio_antiguo = item['precio']
                item['precio'] = nuevo_precio
                print(f"[*] Menú Actualizado en {self.nombre}: '{nombre_plato}' cambió de ${precio_antiguo} a ${nuevo_precio}.")
                return True
        print(f"[x] Error: No se encontró el plato '{nombre_plato}' en el menú.")
        return False

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
        
        # Buscamos la variable 'contraseña'. Si la GUI no la envía, asignamos '1234'
        clave = kwargs.get('contraseña', '1234')
        
        if tipo == "Cliente":
            return Cliente(kwargs['id'], kwargs['nombre'], kwargs['email'], kwargs['direccion'], kwargs.get('contraseña', '1234')) #si no hay contraseña, asigna una genérica 1234
        elif tipo == "Restaurante":
            return Restaurante(kwargs['id'], kwargs['nombre'], kwargs['email'], kwargs.get('menu', []), kwargs.get('contraseña', '1234') )
        elif tipo == "Repartidor":
            return Repartidor(kwargs['id'], kwargs['nombre'], kwargs['email'], kwargs['vehiculo'], kwargs.get('contraseña', '1234'))
        raise ValueError("Tipo de usuario no soportado.")