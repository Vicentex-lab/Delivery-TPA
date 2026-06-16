from typing import List, Optional, Dict
# Importamos las dependencias internas del paquete mediante "relative imports" (.)
from .interfaces import MetodoPago, SistemaNotificacion
from .usuarios import Usuario, Cliente, Restaurante, Repartidor, Pedido

# ==========================================
#LÓGICA DE NEGOCIO
# ==========================================


class GestorPedidos:
    """
    [Patrón Singleton] Garantiza una única instancia del gestor de pedidos.
    [Principio DIP] Depende de la abstracción MetodoPago, no de implementaciones concretas.
    """
    
    _instancia = None
    usuarios_registrados: List[Usuario]
    # Lista adicional para almacenar el histórico de pedidos del sistema
    historial_pedidos: List[Pedido]

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GestorPedidos, cls).__new__(cls)
            cls._instancia.procesadorPago = None 
            cls._instancia.notificador = SistemaNotificacion()
            cls._instancia.usuarios_registrados = []
            cls._instancia.historial_pedidos = []  # Almacena todas las órdenes generadas
        return cls._instancia
    
    def registrar_usuario_sistema(self, usuario: Usuario):
        self.usuarios_registrados.append(usuario)


    #1
    def validar_login(self, nombre_usuario: str, contraseña_ingresada: str) -> Optional[str]: #En la instancia de GestorPedidos, devuelve un string si el login es exitoso o none si falla (type hint)
        for usuario in self.usuarios_registrados: # Para los usuarios de la lista de usuarios registrados 
            if usuario.nombre == nombre_usuario and usuario.contraseña == contraseña_ingresada: # Si ambos coinciden
                print(f"[Login] Acceso concedido a {usuario.nombre} con el rol: {usuario.rol}")
                return usuario.rol #Se devuelve el rol para que la interfaz sepa cual pantalla mostrar
        print(f"[Login Fallido] Intento fallido de inicio de sesión para el usuario: {nombre_usuario}") #Si falla el login
        return None

    def configurar_metodo_pago(self, metodo: MetodoPago):
        self.procesadorPago = metodo

    def formalizar_pedido(self, id_pedido: int, cliente: Cliente, restaurante: Restaurante, items: List[Dict]) -> Pedido:
        """[Funcionalidad 6] Instancia y vincula las entidades dinámicamente en un objeto Pedido"""
        nuevo_pedido = Pedido(id_pedido, cliente, restaurante, items) #A la clase pedido le pasamos los objetos Cliente y Restaurante completos
        self.historial_pedidos.append(nuevo_pedido) # Se guarda el pedido con toda la información en el historial de GestorPedidos
        print(f"[*] Pedido #{id_pedido} formalizado en el sistema para el cliente '{cliente.nombre}'.")
        return nuevo_pedido

    def confirmarPedido(self, pedido: Pedido, cliente: Cliente): #Recibe el objeto Pedido que se quiere procesar y el Cliente
        """[Funcionalidad 14] Asegura la ejecución funcional de la inyección de pagos de la GUI"""
        if not self.procesadorPago: #Si no se ha definido el método de pago, lanza un error
            raise ValueError("Error: Método de pago no configurado en la GUI.")
        
        
        pago_exitoso = self.procesadorPago.procesarPago(pedido.total) #Se procesa el pago según el método de pago escogido y se le pasa el total calculado
        if pago_exitoso: #Definido como True en la GUI
            pedido.actualizarEstado("Confirmado")
            self.notificador.enviarMensaje(cliente.email, f"Tu pedido #{pedido.id} ha sido confirmado.")
        else: #Si fuese False (por fondos insuficientes, por ejemplo)
            pedido.actualizarEstado("Pago Fallido") #No se procesa el pedido

    def cancelar_pedido_rollback(self, pedido: Pedido) -> bool:
        """
        [Funcionalidad 19 - Cancelación (Rollback)]
        Anula un pedido completo únicamente si se encuentra en estado 'Creado' o 'Confirmado'.
        """
        if pedido.estado in ["Creado", "Confirmado"]:
            print(f"[-] Ejecutando Rollback del pedido #{pedido.id}...")
            pedido.actualizarEstado("Cancelado")
            return True
        else:
            print(f"[x] Error en Rollback: No se puede cancelar un pedido que ya está '{pedido.estado}'.")
            return False

    def dar_baja_usuario_soft_delete(self, id_usuario: int) -> bool:
        """
        [Funcionalidad 17 - Baja de Registros (Soft Delete)]
        Elimina un usuario de las listas activas del sistema, validando rigurosamente 
        que no posea ningún pedido activo en curso.
        """
        usuario_a_eliminar = next((u for u in self.usuarios_registrados if u.id == id_usuario), None) #Busca usuario por usuario hasta encontrar al que busca por su ID
        
        if not usuario_a_eliminar:
            print(f"[x] Soft Delete Error: No existe usuario con ID {id_usuario}.")
            return False

        # Validamos si tiene pedidos en curso (cualquier estado que no sea Entregado o Cancelado)
        for p in self.historial_pedidos:
            if (p.cliente == usuario_a_eliminar or p.repartidor == usuario_a_eliminar) and p.estado not in ["Entregado", "Cancelado"]:
                print(f"[x] Soft Delete Denegado: El usuario '{usuario_a_eliminar.nombre}' tiene el pedido #{p.id} en curso ('{p.estado}').") #Busca si el cliente o repartidor tiene un pedido activo, de ser así, deniega la eliminación
                return False

        # Si pasa la validación, se remueve de la lista del sistema activo
        self.usuarios_registrados.remove(usuario_a_eliminar) 
        print(f"[-] Soft Delete Exitoso: El usuario '{usuario_a_eliminar.nombre}' ha sido dado de baja de los registros activos.")
        return True

    
  
