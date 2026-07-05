import json
import os
from typing import List, Optional, Dict
from .interfaces import MetodoPago, SistemaNotificacion
from .usuarios import Usuario, Cliente, Restaurante, Repartidor, Pedido, UsuarioFactory

# ==========================================
# LÓGICA DE NEGOCIO
# ==========================================

class GestorPedidos:
    """
    [Patrón Singleton] Garantiza una única instancia del gestor de pedidos.
    """
    
    _instancia = None
    usuarios_registrados: List[Usuario]
    historial_pedidos: List[Pedido]
    
    ARCHIVO_DATOS = "usuarios_sistema.json"
    ARCHIVO_HISTORIAL = "historial_pedidos.json"

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GestorPedidos, cls).__new__(cls)
            cls._instancia.procesadorPago = None 
            cls._instancia.notificador = SistemaNotificacion()
            cls._instancia.usuarios_registrados = []
            cls._instancia.historial_pedidos = []  
            # Cargar datos automáticamente al iniciar el programa
            cls._instancia.cargar_datos_json()
            cls._instancia.cargar_historial_json()
        return cls._instancia
    
    def registrar_usuario_sistema(self, usuario: Usuario):
        self.usuarios_registrados.append(usuario)
        self.guardar_datos_json()
        
    # --- PERSISTENCIA DE USUARIOS ---
    def guardar_datos_json(self):
        lista_serializada = []
        for u in self.usuarios_registrados:
            datos_usuario = {
                "id": u.id, "nombre": u.nombre, "email": u.email,
                "contraseña": u.contraseña, "rol": u.rol
            }
            if u.rol == "Cliente": datos_usuario["direccion"] = u.direccionEntrega
            elif u.rol == "Restaurante": datos_usuario["menu"] = u.menu
            elif u.rol == "Repartidor": 
                datos_usuario["vehiculo"] = u.vehiculo
                datos_usuario["disponible"] = u.disponible
            lista_serializada.append(datos_usuario)
            
        try:
            with open(self.ARCHIVO_DATOS, "w", encoding="utf-8") as f:
                json.dump(lista_serializada, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[JSON Error] No se pudieron guardar los datos: {e}")

    def cargar_datos_json(self):
        if os.path.exists(self.ARCHIVO_DATOS):
            try:
                with open(self.ARCHIVO_DATOS, 'r', encoding="utf-8") as f:
                    datos = json.load(f)
                    self.usuarios_registrados = [] 
                    for d in datos:
                        nuevo_usuario = UsuarioFactory.crear_usuario(tipo=d["rol"], **d)
                        if d["rol"] == "Repartidor":
                            nuevo_usuario.disponible = d.get("disponible", True)
                        self.usuarios_registrados.append(nuevo_usuario)
                print(f"[JSON] {len(self.usuarios_registrados)} usuarios restaurados.")
            except Exception as e:
                print(f"Error cargando JSON de usuarios: {e}")

    # --- PERSISTENCIA DE PEDIDOS (NUEVO) ---
    def guardar_historial_json(self):
        lista_serializada = []
        for p in self.historial_pedidos:
            datos_pedido = {
                "id": p.id,
                "estado": p.estado,
                "subtotal": p.subtotal,
                "total": p.total,
                "tarifa_envio": p.tarifa_envio,
                "propina": p.propina,
                "cliente_id": p.cliente.id if p.cliente else None,
                "restaurante_id": p.restaurante.id if p.restaurante else None,
                "repartidor_id": p.repartidor.id if p.repartidor else None,
                "items_comprados": p.items_comprados
            }
            lista_serializada.append(datos_pedido)
        try:
            with open(self.ARCHIVO_HISTORIAL, "w", encoding="utf-8") as f:
                json.dump(lista_serializada, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[JSON Error] Historial no guardado: {e}")

    def cargar_historial_json(self):
        if os.path.exists(self.ARCHIVO_HISTORIAL):
            try:
                with open(self.ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
                    lista_diccionarios = json.load(f)
                
                self.historial_pedidos = []
                for d in lista_diccionarios:
                    cliente = next((u for u in self.usuarios_registrados if u.id == d["cliente_id"]), None)
                    restaurante = next((u for u in self.usuarios_registrados if u.id == d["restaurante_id"]), None)
                    repartidor = next((u for u in self.usuarios_registrados if u.id == d["repartidor_id"]), None)
                    
                    if cliente and restaurante:
                        pedido = Pedido(d["id"], cliente, restaurante, d["items_comprados"])
                        pedido.estado = d["estado"]
                        pedido.subtotal = d["subtotal"]
                        pedido.total = d["total"]
                        pedido.tarifa_envio = d["tarifa_envio"]
                        pedido.propina = d["propina"]
                        pedido.repartidor = repartidor
                        self.historial_pedidos.append(pedido)
                print(f"[JSON] {len(self.historial_pedidos)} pedidos restaurados.")
            except Exception as e:
                print(f"Error cargando historial de pedidos: {e}")

    # --- LÓGICA CORE ---
    def validar_login(self, nombre_usuario: str, contraseña_ingresada: str) -> Optional[str]: 
        for usuario in self.usuarios_registrados: 
            if usuario.nombre == nombre_usuario and usuario.contraseña == contraseña_ingresada: 
                return usuario.rol 
        return None

    def configurar_metodo_pago(self, metodo: MetodoPago):
        self.procesadorPago = metodo

    def formalizar_pedido(self, id_pedido: int, cliente: Cliente, restaurante: Restaurante, items: List[Dict]) -> Pedido:
        nuevo_pedido = Pedido(id_pedido, cliente, restaurante, items)
        self.historial_pedidos.append(nuevo_pedido)
        self.guardar_historial_json()
        return nuevo_pedido

    def confirmarPedido(self, pedido: Pedido, cliente: Cliente): 
        if not self.procesadorPago: 
            raise ValueError("Error: Método de pago no configurado.")
        
        pago_exitoso = self.procesadorPago.procesarPago(pedido.total) 
        if pago_exitoso: 
            pedido.actualizarEstado("Confirmado")
            self.notificador.enviarMensaje(cliente.email, f"Tu pedido #{pedido.id} ha sido confirmado.")
            self.guardar_historial_json()
        else: 
            pedido.actualizarEstado("Pago Fallido") 

    def cancelar_pedido_rollback(self, pedido: Pedido) -> bool:
        if pedido.estado in ["Creado", "Confirmado"]:
            pedido.actualizarEstado("Cancelado")
            self.guardar_historial_json()
            return True
        return False

    def dar_baja_usuario_soft_delete(self, id_usuario: int) -> bool:
        usuario_a_eliminar = next((u for u in self.usuarios_registrados if u.id == id_usuario), None) 
        if not usuario_a_eliminar: return False

        for p in self.historial_pedidos:
            if (p.cliente == usuario_a_eliminar or p.repartidor == usuario_a_eliminar) and p.estado not in ["Entregado", "Cancelado", "Rechazado"]:
                return False

        self.usuarios_registrados.remove(usuario_a_eliminar)
        self.guardar_datos_json() 
        return True