from .logica_negocio import GestorPedidos
from .usuarios import UsuarioFactory
from .interfaces import PagoTarjeta, PagoPaypal

class SistemaDeliveryFacade:
    """
    [Patrón Estructural: Facade]
    Proporciona una interfaz unificada y de alto nivel que hace que el 
    subsistema sea más fácil de usar, reduciendo el acoplamiento con la GUI.
    """
    def __init__(self):
        self.gestor = GestorPedidos()
        # El Facade ahora administra el estado, liberando a la GUI de esta responsabilidad
        self.clientes = []
        self.restaurantes = []
        self.repartidores = []
        self._inicializar_admin()

    def _inicializar_admin(self):
        usuario_prueba = UsuarioFactory.crear_usuario(
            "Cliente", id=0, nombre="admin", email="admin@mail.com",
            direccion="Admin", contraseña="1234"
        )
        self.gestor.registrar_usuario_sistema(usuario_prueba)

    def login(self, usuario, contrasena):
        return self.gestor.validar_login(usuario, contrasena)

    # --- DELEGACIÓN DE CREACIÓN (Ocultando el Factory a la GUI) ---
    def registrar_cliente(self, id_usuario, nombre, email, direccion, contrasena):
        cliente = UsuarioFactory.crear_usuario("Cliente", id=id_usuario, nombre=nombre, email=email, direccion=direccion, contraseña=contrasena)
        self.clientes.append(cliente)
        self.gestor.registrar_usuario_sistema(cliente)
        return cliente

    def registrar_restaurante(self, id_usuario, nombre, email, menu):
        restaurante = UsuarioFactory.crear_usuario("Restaurante", id=id_usuario, nombre=nombre, email=email, menu=menu)
        self.restaurantes.append(restaurante)
        self.gestor.registrar_usuario_sistema(restaurante)
        return restaurante

    def registrar_repartidor(self, id_usuario, nombre, email, vehiculo, contrasena):
        repartidor = UsuarioFactory.crear_usuario("Repartidor", id=id_usuario, nombre=nombre, email=email, vehiculo=vehiculo, contraseña=contrasena)
        self.repartidores.append(repartidor)
        self.gestor.registrar_usuario_sistema(repartidor)
        return repartidor

    # --- ORQUESTACIÓN COMPLEJA
    def procesar_compra_completa(self, id_pedido, cliente, restaurante, carrito, metodo_pago_str):
        """Coordina el Factory, Gestor de Pedidos, Pagos y Repartidores en un solo llamado."""
        
        repartidor = next((r for r in self.repartidores if r.disponible), None)
        if not repartidor:
            return False, "No hay repartidores disponibles en este momento."

        # Inyección de dependencias oculta a la GUI
        metodo = PagoTarjeta() if metodo_pago_str == "Tarjeta de Crédito" else PagoPaypal()
        self.gestor.configurar_metodo_pago(metodo)

        # Formalizar y procesar
        pedido = self.gestor.formalizar_pedido(id_pedido, cliente, restaurante, carrito)
        pedido.repartidor = repartidor
        repartidor.disponible = False
        
        pedido.calcularTotal()
        
        # Flujo de estados centralizado
        self.gestor.confirmarPedido(pedido, cliente)
        restaurante.prepararPedido(pedido)
        pedido.actualizarEstado("En Camino")
        repartidor.actualizarUbicacion()
        repartidor.completarEntrega(pedido)

        return True, pedido