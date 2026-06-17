# Importamos lo necesario desde la carpeta backend
from backend.logica_negocio import GestorPedidos
from backend.usuarios import UsuarioFactory
from backend.interfaces import PagoPaypal, CargoServicioDecorator

# ==========================================
# SCRIPT DE PRUEBA: 20 FUNCIONALIDADES
# ==========================================
if __name__ == "__main__":
    print("\n==================================================")
    print("--- COMPROBACIÓN REQUERIMIENTOS VICENTE CÁRDENAS ---")
    print("==================================================")
    
    gestor_sistema = GestorPedidos()

    # --- INSTANCIACIÓN REQUERIDA PARA LAS PRUEBAS ---
    # Creamos las entidades base asegurando el uso del parámetro 'contraseña'
    cliente1 = UsuarioFactory.crear_usuario(
        "Cliente", id=1, nombre="Antonia", email="antonia@mail.com", 
        direccion="Manuel Rodriguez 1874", contraseña="securePass123"
    )
    
    menu_italiano = [{'item': 'Pizza Margarita', 'precio': 12.5}, {'item': 'Palitos de ajo', 'precio': 5.0}]
    restaurante1 = UsuarioFactory.crear_usuario(
        "Restaurante", id=101, nombre="Papa Johns", email="contacto@papajohns.com", menu=menu_italiano
    )
    
    repartidor1 = UsuarioFactory.crear_usuario(
        "Repartidor", id=201, nombre="Esteban", email="esteban@delivery.com", vehiculo="Moto Suzuki"
    )

    # ==================================================
    # PRUEBA DE FUNCIONALIDAD 1: VALIDACIÓN DE LOGIN
    # ==================================================
    print("\n-> Probando Funcionalidad 1 (Login):")
    # Registramos al cliente en la persistencia del sistema activo
    gestor_sistema.registrar_usuario_sistema(cliente1)
    
    # Caso 1: Login Fallido
    gestor_sistema.validar_login("Antonia", "clave_incorrecta")
    # Caso 2: Login Exitoso (Debe retornar 'Cliente')
    gestor_sistema.validar_login("Antonia", "securePass123")

    # ==================================================
    # PRUEBAS RESTO DE REQUERIMIENTOS
    # ==================================================
    
    # Probar Funcionalidades 11 y 12 (Actualizaciones)
    print("\n-> Probando Funcionalidades 11 y 12:")
    cliente1.actualizar_direccion("Nueva Avenida Diagonal 456")
    restaurante1.modificar_item("Pizza Margarita", 14.99)

    # Probar Funcionalidad 6 (Formalización dinámica)
    print("\n-> Probando Funcionalidad 6:")
    pedido_dinamico = gestor_sistema.formalizar_pedido(2002, cliente1, restaurante1, [restaurante1.menu[0]])

    # Probar Funcionalidad 13 (Cálculo Avanzado con Extras)
    print("\n-> Probando Funcionalidad 13:")
    total_con_extras = pedido_dinamico.calcularTotal(tarifa_envio=2.50, propina=1.50)
    print(f"Subtotal: ${pedido_dinamico.subtotal:.2f} | Envío: $2.50 | Propina: $1.50")
    print(f"Total Neto Calculado: ${total_con_extras:.2f}")

    # Probar Funcionalidades 15 y 16 (Sincronización Automática de Repartidor)
    print("\n-> Probando Funcionalidades 15 y 16:")
    pedido_dinamico.repartidor = repartidor1
    print(f"Estado inicial de {repartidor1.nombre} antes de confirmar: Disponible = {repartidor1.disponible}")
        
    #gestor_sistema.configurar_metodo_pago(PagoPaypal())
    pago_base = PagoPaypal()
    pago_con_cargo = CargoServicioDecorator(pago_base)
    gestor_sistema.configurar_metodo_pago(pago_con_cargo)
    gestor_sistema.confirmarPedido(pedido_dinamico, cliente1)
    print(f"Estado de {repartidor1.nombre} tras confirmar el pedido: Disponible = {repartidor1.disponible} (Debe ser False)")
        
    # Cambiamos a entregado para liberar al repartidor automáticamente
    pedido_dinamico.actualizarEstado("Entregado")
    print(f"Estado de {repartidor1.nombre} tras entrega completada: Disponible = {repartidor1.disponible} (Debe ser True)")

    # Probar Funcionalidad 19 (Rollback)
    print("\n-> Probando Funcionalidad 19:")
    pedido_cancelable = gestor_sistema.formalizar_pedido(3003, cliente1, restaurante1, [restaurante1.menu[0]])
    # Intentamos cancelarlo cuando está en estado "Creado"
    gestor_sistema.cancelar_pedido_rollback(pedido_cancelable)

    # Probar Funcionalidad 17 (Soft Delete con validación)
    print("\n-> Probando Funcionalidad 17:")
    # Creamos un pedido que se quede "En Preparación" asignado a Antonia
    pedido_activo = gestor_sistema.formalizar_pedido(4004, cliente1, restaurante1, [restaurante1.menu[0]])
    pedido_activo.actualizarEstado("En Preparación")
        
    # Intento 1: Debe denegarse porque tiene el pedido 4004 activo
    gestor_sistema.dar_baja_usuario_soft_delete(cliente1.id)
        
    # Intento 2: Lo cancelamos (Rollback) y ahora sí debería permitir la baja lógica
    gestor_sistema.cancelar_pedido_rollback(pedido_activo)
    gestor_sistema.dar_baja_usuario_soft_delete(cliente1.id)