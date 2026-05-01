import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Importamos las clases intactas desde tu backend
from backend import (UsuarioFactory, GestorPedidos, Pedido, 
                     PagoTarjeta, PagoPaypal)

class ConsolaRedirector:
    """Redirige el stdout (print) al widget Text de Tkinter."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, mensaje):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, mensaje)
        self.text_widget.see(tk.END) # Auto-scroll
        self.text_widget.configure(state='disabled')

    def flush(self):
        pass

class DeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Delivery - Panel de Control")
        self.root.geometry("850x650")
        
        # Estado de la aplicación (Simulando la base de datos)
        self.clientes = []
        self.restaurantes = []
        self.repartidores = []
        self.carrito = []
        
        # Instancia Singleton del Gestor
        self.gestor = GestorPedidos()

        self._configurar_estilos()
        self._crear_interfaz()
        
        # Redirigir consola a la Pestaña 3
        sys.stdout = ConsolaRedirector(self.consola_text)
        
        print("--- SISTEMA DE DELIVERY INICIADO (GUI) ---")

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', padding=[15, 5], font=('Helvetica', 10, 'bold'))
        style.configure('TButton', padding=6, font=('Helvetica', 10))
        style.configure('TLabelframe', font=('Helvetica', 11, 'bold'))

    def _crear_interfaz(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Creación de Pestañas
        self.tab_gestion = ttk.Frame(notebook)
        self.tab_pedido = ttk.Frame(notebook)
        self.tab_consola = ttk.Frame(notebook)

        notebook.add(self.tab_gestion, text='👤 1. Gestión (CRUD)')
        notebook.add(self.tab_pedido, text='🛒 2. Nuevo Pedido')
        notebook.add(self.tab_consola, text='🖥️ 3. Consola / Tracking')

        self._construir_tab_gestion()
        self._construir_tab_pedido()
        self._construir_tab_consola()

    # ==========================================
    # PESTAÑA 1: GESTIÓN (CRUD Simulado)
    # ==========================================
    def _construir_tab_gestion(self):
        frame = ttk.LabelFrame(self.tab_gestion, text="Creación Rápida de Entidades", padding=20)
        frame.pack(fill='x', padx=20, pady=20)

        btn_cliente = ttk.Button(frame, text="Crear Cliente (Ana)", command=self._crear_cliente)
        btn_cliente.pack(side='left', padx=10, expand=True)

        btn_restaurante = ttk.Button(frame, text="Crear Restaurante (Luigi's)", command=self._crear_restaurante)
        btn_restaurante.pack(side='left', padx=10, expand=True)

        btn_repartidor = ttk.Button(frame, text="Crear Repartidor (Carlos)", command=self._crear_repartidor)
        btn_repartidor.pack(side='left', padx=10, expand=True)

    def _crear_cliente(self):
        cliente = UsuarioFactory.crear_usuario("Cliente", id=1, nombre="Ana", email="ana@mail.com", direccion="Av. Siempre Viva 123")
        self.clientes.append(cliente)
        print(f"[*] Creado: {cliente.obtenerDatos()}")

    def _crear_restaurante(self):
        menu_italiano = [{'item': 'Pizza Margarita', 'precio': 12.5}, {'item': 'Lasagna', 'precio': 15.0}]
        restaurante = UsuarioFactory.crear_usuario("Restaurante", id=101, nombre="Luigi's", email="contacto@luigis.com", menu=menu_italiano)
        self.restaurantes.append(restaurante)
        self.combo_restaurantes['values'] = [r.nombre for r in self.restaurantes] # Actualizar UI de pedidos
        print(f"[*] Creado: {restaurante.obtenerDatos()}")

    def _crear_repartidor(self):
        repartidor = UsuarioFactory.crear_usuario("Repartidor", id=201, nombre="Carlos", email="carlos@delivery.com", vehiculo="Moto Honda")
        self.repartidores.append(repartidor)
        print(f"[*] Creado: {repartidor.obtenerDatos()}")

    # ==========================================
    # PESTAÑA 2: NUEVO PEDIDO
    # ==========================================
    def _construir_tab_pedido(self):
        # Selección de Restaurante
        frame_rest = ttk.LabelFrame(self.tab_pedido, text="Selección de Restaurante", padding=10)
        frame_rest.pack(fill='x', padx=20, pady=10)
        
        self.combo_restaurantes = ttk.Combobox(frame_rest, state="readonly")
        self.combo_restaurantes.pack(side='left', padx=10)
        self.combo_restaurantes.bind("<<ComboboxSelected>>", self._cargar_menu)

        # Menú y Carrito
        frame_menu = ttk.Frame(self.tab_pedido)
        frame_menu.pack(fill='both', expand=True, padx=20, pady=5)

        # Lista de Menú
        lbl_menu = ttk.LabelFrame(frame_menu, text="Menú Disponible", padding=10)
        lbl_menu.pack(side='left', fill='both', expand=True, padx=5)
        self.lista_menu = tk.Listbox(lbl_menu, height=8)
        self.lista_menu.pack(fill='both', expand=True)
        btn_agregar = ttk.Button(lbl_menu, text="Añadir al Carrito ->", command=self._agregar_al_carrito)
        btn_agregar.pack(pady=5)

        # Lista de Carrito
        lbl_carrito = ttk.LabelFrame(frame_menu, text="Tu Carrito", padding=10)
        lbl_carrito.pack(side='right', fill='both', expand=True, padx=5)
        self.lista_carrito = tk.Listbox(lbl_carrito, height=8)
        self.lista_carrito.pack(fill='both', expand=True)

        # Pago y Confirmación
        frame_pago = ttk.LabelFrame(self.tab_pedido, text="Pago y Confirmación", padding=10)
        frame_pago.pack(fill='x', padx=20, pady=10)

        ttk.Label(frame_pago, text="Método de Pago:").pack(side='left', padx=5)
        self.combo_pago = ttk.Combobox(frame_pago, values=["Tarjeta de Crédito", "PayPal"], state="readonly")
        self.combo_pago.pack(side='left', padx=5)
        self.combo_pago.current(0)

        btn_confirmar = ttk.Button(frame_pago, text="Pagar y Confirmar Pedido", command=self._procesar_pedido)
        btn_confirmar.pack(side='right', padx=10)

    def _cargar_menu(self, event):
        self.lista_menu.delete(0, tk.END)
        nombre_rest = self.combo_restaurantes.get()
        restaurante = next((r for r in self.restaurantes if r.nombre == nombre_rest), None)
        
        if restaurante:
            for item in restaurante.menu:
                self.lista_menu.insert(tk.END, f"{item['item']} - ${item['precio']}")

    def _agregar_al_carrito(self):
        seleccion = self.lista_menu.curselection()
        if not seleccion:
            return
        
        index = seleccion[0]
        nombre_rest = self.combo_restaurantes.get()
        restaurante = next((r for r in self.restaurantes if r.nombre == nombre_rest), None)
        
        if restaurante:
            item = restaurante.menu[index]
            self.carrito.append(item)
            self.lista_carrito.insert(tk.END, f"{item['item']} - ${item['precio']}")

    def _procesar_pedido(self):
        if not self.clientes or not self.repartidores:
            messagebox.showwarning("Atención", "Debes crear al menos un Cliente y un Repartidor en la Pestaña 1.")
            return
        if not self.carrito:
            messagebox.showwarning("Atención", "El carrito está vacío.")
            return

        cliente = self.clientes[0] # Tomamos el primer cliente creado
        nombre_rest = self.combo_restaurantes.get()
        restaurante = next((r for r in self.restaurantes if r.nombre == nombre_rest), None)

        print("\n--- INICIANDO PROCESO DE COMPRA ---")
        cliente.realizarPedido()
        
        # 1. Crear Pedido
        pedido = Pedido(id_pedido=1001, cliente=cliente, restaurante=restaurante, items_comprados=self.carrito.copy())
        total = pedido.calcularTotal()
        print(f"Total a pagar: ${total:.2f}")

        # 2. Asignar Repartidor
        repartidor = next((r for r in self.repartidores if r.disponible), None)
        if repartidor:
            pedido.repartidor = repartidor
            repartidor.disponible = False
            print(f"Asignación Automática: Repartidor {repartidor.nombre} asignado.")
        else:
            print("❌ No hay repartidores disponibles.")
            return

        # 3. Inyección de Dependencias (Estrategia de Pago)
        metodo = PagoTarjeta() if self.combo_pago.get() == "Tarjeta de Crédito" else PagoPaypal()
        self.gestor.configurar_metodo_pago(metodo)

        # 4. Confirmar y simular flujo
        self.gestor.confirmarPedido(pedido, cliente)
        restaurante.prepararPedido(pedido)
        pedido.actualizarEstado("En Camino")
        repartidor.actualizarUbicacion()
        repartidor.completarEntrega(pedido)

        # Limpiar carrito
        self.carrito.clear()
        self.lista_carrito.delete(0, tk.END)
        messagebox.showinfo("Éxito", "¡Pedido procesado con éxito! Revisa la consola.")

    # ==========================================
    # PESTAÑA 3: CONSOLA DE EVENTOS
    # ==========================================
    def _construir_tab_consola(self):
        self.consola_text = tk.Text(self.tab_consola, bg="black", fg="#00FF00", font=('Courier', 10), state='disabled', wrap='word')
        scrollbar = ttk.Scrollbar(self.tab_consola, orient='vertical', command=self.consola_text.yview)
        
        self.consola_text.configure(yscrollcommand=scrollbar.set)
        self.consola_text.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = DeliveryApp(root)
    root.mainloop()