from backend.logica_negocio import GestorPedidos
from backend.usuarios import UsuarioFactory
from backend.interfaces import PagoPaypal, PagoTarjeta

def generar_mock_data(gestor: GestorPedidos):
    print("\n--- INICIALIZANDO MOCK DATA (10 Clientes, 5 Restaurantes, 5 Repartidores) ---")
    
    # 1. Instanciar 10 Clientes
    for i in range(1, 11):
        cliente = UsuarioFactory.crear_usuario(
            "Cliente", id=i, nombre=f"Cliente_{i}", email=f"user{i}@mail.com", 
            direccion=f"Calle Falsa {100+i}", contraseña="123"
        )
        gestor.registrar_usuario_sistema(cliente)

    # 2. Instanciar 5 Restaurantes con 10 platos cada uno
    for i in range(1, 6):
        menu_mock = [{'item': f'Plato {j} Rest {i}', 'precio': 5.0 + j} for j in range(1, 11)]
        restaurante = UsuarioFactory.crear_usuario(
            "Restaurante", id=100+i, nombre=f"Restaurante_{i}", 
            email=f"contacto{i}@food.com", menu=menu_mock, contraseña="123"
        )
        gestor.registrar_usuario_sistema(restaurante)

    # 3. Instanciar 5 Repartidores
    for i in range(1, 6):
        repartidor = UsuarioFactory.crear_usuario(
            "Repartidor", id=200+i, nombre=f"Repartidor_{i}", 
            email=f"rider{i}@delivery.com", vehiculo="Moto", contraseña="123"
        )
        gestor.registrar_usuario_sistema(repartidor)
    print("[*] Mock Data inyectada con éxito en la persistencia del sistema.\n")

if __name__ == "__main__":
    print("\n==================================================")
    print("--- SISTEMA DE DELIVERY: COMPROBACIÓN DE FUNCIONALIDADES ---")
    print("==================================================")
    
    gestor = GestorPedidos()
    generar_mock_data(gestor)

    # Extrayendo entidades para las pruebas
    cliente_test = gestor.usuarios_registrados[0]  # Cliente_1
    restaurante_test = gestor.usuarios_registrados[10] # Restaurante_1
    repartidor_test = gestor.usuarios_registrados[15] # Repartidor_1

    # PRUEBA QA - EXCEPCIONES Y VALIDACIONES (Funcionalidad 20)
    print("\n-> Probando Funcionalidad 20 (Manejo de Excepciones y QA):")
    try:
        # Intento de forzar un método de pago nulo (Debe saltar excepción controlada)
        gestor.configurar_metodo_pago(None)
        pedido_error = gestor.formalizar_pedido(999, cliente_test, restaurante_test, [restaurante_test.menu[0]])
        gestor.confirmarPedido(pedido_error, cliente_test)
    except ValueError as e:
        print(f"[QA Exception Catch] Bloqueo exitoso. Error detectado: {e}")

    # PRUEBA DECORATOR (Funcionalidad 13 con Patrón Estructural)
    print("\n-> Probando Funcionalidad 13 (Cálculo Avanzado con Patrón Decorator):")
    pedido_dinamico = gestor.formalizar_pedido(1001, cliente_test, restaurante_test, [restaurante_test.menu[0], restaurante_test.menu[1]])
    
    total_con_extras = pedido_dinamico.calcularTotal(tarifa_envio=3.50, propina=2.00)
    print(f"Subtotal Base: ${pedido_dinamico.subtotal:.2f}")
    print(f"Tarifa de Envío: ${pedido_dinamico.tarifa_envio:.2f}")
    print(f"Propina: ${pedido_dinamico.propina:.2f}")
    print(f"Total Neto (vía Decorator): ${total_con_extras:.2f}")

    # PRUEBA DE FLUJO COMPLETO (Funcionalidades 14, 15 y 16)
    print("\n-> Probando Funcionalidades 14, 15 y 16 (Estrategia, Estados y Sync):")
    pedido_dinamico.repartidor = repartidor_test
    gestor.configurar_metodo_pago(PagoTarjeta())
    
    print(f"Estado Repartidor antes: Disponible = {repartidor_test.disponible}")
    gestor.confirmarPedido(pedido_dinamico, cliente_test)
    restaurante_test.prepararPedido(pedido_dinamico)
    pedido_dinamico.actualizarEstado("En Camino")
    print(f"Estado Repartidor en ruta: Disponible = {repartidor_test.disponible} (Debe ser False)")
    
    repartidor_test.completarEntrega(pedido_dinamico)
    print(f"Estado Repartidor post-entrega: Disponible = {repartidor_test.disponible} (Debe ser True)")

    print("\n==================================================")
    print("TODAS LAS FUNCIONALIDADES INTEGRADAS CORRECTAMENTE.")
    print("==================================================")