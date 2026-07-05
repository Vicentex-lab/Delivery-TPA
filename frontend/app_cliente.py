import tkinter as tk
from tkinter import ttk, messagebox
from backend.usuarios import Pedido
from backend.interfaces import PagoTarjeta, PagoPaypal, CargoServicioDecorator

class ClienteApp:
    def __init__(self, root, cliente, gestor, callback_logout):
        self.root = root
        self.cliente = cliente
        self.gestor = gestor
        self.callback_logout = callback_logout
        self.carrito = []

        self.root.title(f"Sistema de Delivery - Panel Cliente | {self.cliente.nombre}")
        self.root.geometry("850x650")
        self.restaurantes = [u for u in self.gestor.usuarios_registrados if u.rol == "Restaurante"]

        self._configurar_estilos()
        self._crear_interfaz()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        BG_COLOR = "#2B2B2B"
        FG_COLOR = "#FFFFFF"
        ACCENT_COLOR = "#FF6B35"
        BTN_BG = "#3C3F41"
        TREE_BG = "#333333"

        style.configure('.', background=BG_COLOR, foreground=FG_COLOR, font=('Helvetica', 10))
        self.root.configure(bg=BG_COLOR)
        style.configure('TNotebook', background=BG_COLOR, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[15, 5], font=('Helvetica', 10, 'bold'), background=BTN_BG, foreground=FG_COLOR, borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', ACCENT_COLOR)], foreground=[('selected', '#FFFFFF')])
        style.configure('TButton', padding=6, font=('Helvetica', 10, 'bold'), background=BTN_BG, foreground=FG_COLOR, borderwidth=1, bordercolor=BG_COLOR)
        style.map('TButton', background=[('active', ACCENT_COLOR)], foreground=[('active', '#FFFFFF')])
        style.configure('TLabelframe', background=BG_COLOR, bordercolor=BTN_BG, borderwidth=2)
        style.configure('TLabelframe.Label', font=('Helvetica', 11, 'bold'), background=BG_COLOR, foreground=ACCENT_COLOR)
        style.configure('Treeview', background=TREE_BG, foreground=FG_COLOR, fieldbackground=TREE_BG, rowheight=30, borderwidth=0)
        style.configure('Treeview.Heading', background=BTN_BG, foreground=FG_COLOR, font=('Helvetica', 10, 'bold'), borderwidth=1)
        style.map('Treeview', background=[('selected', ACCENT_COLOR)])

    def _crear_interfaz(self):
        # Header de Sesión
        header = ttk.Frame(self.root)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"👤 Cliente: {self.cliente.nombre}", font=('Helvetica', 11, 'bold')).pack(side='left')
        ttk.Button(header, text="🚪 Cerrar Sesión", command=self.callback_logout).pack(side='right')

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)

        self.tab_pedido = ttk.Frame(notebook)
        self.tab_historial = ttk.Frame(notebook)

        notebook.add(self.tab_pedido, text=' 🍔 Hacer Pedido')
        notebook.add(self.tab_historial, text=' 📜 Mis Pedidos')

        self._construir_tab_pedido()
        self._construir_tab_historial()
        self._actualizar_historial()

    # --- RESTO DEL CÓDIGO IGUAL A LA VERSIÓN ANTERIOR EXCEPTO EN GUARDAR ---
    def _construir_tab_pedido(self):
        frame_rest = ttk.LabelFrame(self.tab_pedido, text="Selección de Restaurante", padding=10)
        frame_rest.pack(fill='x', padx=20, pady=10)
        self.combo_restaurantes = ttk.Combobox(frame_rest, values=[r.nombre for r in self.restaurantes], state="readonly")
        self.combo_restaurantes.pack(side='left', padx=10)
        self.combo_restaurantes.bind("<<ComboboxSelected>>", self._cargar_menu)

        frame_menu = ttk.Frame(self.tab_pedido)
        frame_menu.pack(fill='both', expand=True, padx=20, pady=5)

        lbl_menu = ttk.LabelFrame(frame_menu, text="Menú Disponible", padding=10)
        lbl_menu.pack(side='left', fill='both', expand=True, padx=5)
        self.lista_menu = tk.Listbox(lbl_menu, height=8, bg="#333333", fg="#FFFFFF", selectbackground="#FF6B35", borderwidth=0)
        self.lista_menu.pack(fill='both', expand=True)
        ttk.Button(lbl_menu, text="Añadir al Carrito ->", command=self._agregar_al_carrito).pack(pady=5)

        lbl_carrito = ttk.LabelFrame(frame_menu, text="Tu Carrito", padding=10)
        lbl_carrito.pack(side='right', fill='both', expand=True, padx=5)
        self.lista_carrito = tk.Listbox(lbl_carrito, height=8)
        self.lista_carrito.pack(fill='both', expand=True)

        frame_botones_carrito = ttk.Frame(lbl_carrito)
        frame_botones_carrito.pack(fill='x', pady=5)
        ttk.Button(frame_botones_carrito, text="Eliminar ítem", command=self._eliminar_del_carrito).pack(side='left', expand=True, padx=2)
        ttk.Button(frame_botones_carrito, text="Vaciar carrito", command=self._vaciar_carrito).pack(side='right', expand=True, padx=2)

        frame_pago = ttk.LabelFrame(self.tab_pedido, text="Pago y Confirmación", padding=10)
        frame_pago.pack(fill='x', padx=20, pady=10)
        ttk.Label(frame_pago, text="Método de Pago:").pack(side='left', padx=5)
        self.combo_pago = ttk.Combobox(frame_pago, values=["Tarjeta de Crédito", "PayPal"], state="readonly")
        self.combo_pago.pack(side='left', padx=5)
        self.combo_pago.current(0)
        ttk.Button(frame_pago, text="Pagar y Enviar Pedido", command=self._procesar_pedido).pack(side='right', padx=10)

    def _cargar_menu(self, event):
        self.lista_menu.delete(0, tk.END)
        rest = next((r for r in self.restaurantes if r.nombre == self.combo_restaurantes.get()), None)
        if rest:
            for item in rest.menu: self.lista_menu.insert(tk.END, f"{item['item']} - ${item['precio']}")

    def _agregar_al_carrito(self):
        sel = self.lista_menu.curselection()
        if not sel: return
        rest = next((r for r in self.restaurantes if r.nombre == self.combo_restaurantes.get()), None)
        if rest:
            item = rest.menu[sel[0]]
            self.carrito.append(item)
            self.lista_carrito.insert(tk.END, f"{item['item']} - ${item['precio']}")

    def _eliminar_del_carrito(self):
        sel = self.lista_carrito.curselection()
        if not sel: return
        self.carrito.pop(sel[0])
        self.lista_carrito.delete(sel[0])

    def _vaciar_carrito(self):
        self.carrito.clear()
        self.lista_carrito.delete(0, tk.END)

    def _procesar_pedido(self):
        if not self.carrito: return
        rest = next((r for r in self.restaurantes if r.nombre == self.combo_restaurantes.get()), None)
        
        nuevo_id = len(self.gestor.historial_pedidos) + 1 
        pedido = Pedido(id_pedido=nuevo_id, cliente=self.cliente, restaurante=rest, items_comprados=list(self.carrito))
        pedido.calcularTotal()

        metodo_base = PagoTarjeta() if self.combo_pago.get() == "Tarjeta de Crédito" else PagoPaypal()
        self.gestor.configurar_metodo_pago(CargoServicioDecorator(metodo_base))
        self.gestor.confirmarPedido(pedido, self.cliente)
        
        self.gestor.historial_pedidos.append(pedido)
        self.gestor.guardar_historial_json() 

        # --- AQUÍ GENERAMOS EL PDF ---
        self._generar_boleta_pdf(pedido)

        self._vaciar_carrito()
        self._actualizar_historial()
        
        # Mensaje actualizado avisando de la boleta
        messagebox.showinfo("Éxito", f"¡Pedido #{pedido.id} enviado al restaurante!\n\nSe ha generado el archivo PDF con tu boleta de compra.")

    def _construir_tab_historial(self):
        frame_acciones = ttk.Frame(self.tab_historial)
        frame_acciones.pack(fill='x', padx=20, pady=(15, 0))
        ttk.Button(frame_acciones, text="🔄 Refrescar", command=self._actualizar_historial).pack(side='left', padx=5)
        ttk.Button(frame_acciones, text="❌ Cancelar Pedido Seleccionado", command=self._cancelar_pedido).pack(side='right', padx=5)

        frame_tabla = ttk.LabelFrame(self.tab_historial, text="Mis Pedidos", padding=10)
        frame_tabla.pack(fill='both', expand=True, padx=20, pady=10)
        self.tree_historial = ttk.Treeview(frame_tabla, columns=('ID', 'Rest', 'Rep', 'Total', 'Estado'), show='headings', height=14)
        
        self.tree_historial.heading('ID', text='ID'); self.tree_historial.column('ID', width=40, anchor='center')
        self.tree_historial.heading('Rest', text='Restaurante'); self.tree_historial.column('Rest', width=150)
        self.tree_historial.heading('Rep', text='Repartidor'); self.tree_historial.column('Rep', width=150)
        self.tree_historial.heading('Total', text='Total'); self.tree_historial.column('Total', width=80, anchor='center')
        self.tree_historial.heading('Estado', text='Estado'); self.tree_historial.column('Estado', width=120, anchor='center')

        self.tree_historial.pack(fill='both', expand=True)

    def _actualizar_historial(self):
        for i in self.tree_historial.get_children(): self.tree_historial.delete(i)
        for p in [p for p in self.gestor.historial_pedidos if p.cliente.id == self.cliente.id]:
            self.tree_historial.insert('', tk.END, values=(f"{p.id}", p.restaurante.nombre, p.repartidor.nombre if p.repartidor else "Pendiente", f"${p.total:.2f}", p.estado))

    def _cancelar_pedido(self):
        sel = self.tree_historial.selection()
        if not sel: return
        pedido = next((p for p in self.gestor.historial_pedidos if p.id == int(self.tree_historial.item(sel[0], 'values')[0])), None)
        
        if pedido and self.gestor.cancelar_pedido_rollback(pedido):
            messagebox.showinfo("Cancelado", "Pedido cancelado exitosamente.")
            self._actualizar_historial()
        else:
            messagebox.showerror("No se puede cancelar", f"Su estado actual es: '{pedido.estado}'.")
            
    def _generar_boleta_pdf(self, pedido):
        try:
            from fpdf import FPDF
        except ImportError:
            print("[Advertencia] No se pudo generar la boleta. Falta instalar 'fpdf'.")
            return

        pdf = FPDF()
        pdf.add_page()
        
        # Título de la Boleta
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "BOLETA DE VENTA - DELIVERY APP", ln=True, align='C')
        pdf.ln(5)
        
        # Datos Generales
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, f"Nro. de Pedido: #{pedido.id}", ln=True)
        pdf.cell(0, 8, f"Cliente: {pedido.cliente.nombre} ({pedido.cliente.email})", ln=True)
        pdf.cell(0, 8, f"Restaurante: {pedido.restaurante.nombre}", ln=True)
        pdf.cell(0, 8, f"Dirección de Entrega: {pedido.cliente.direccionEntrega}", ln=True)
        
        pdf.line(10, 60, 200, 60)
        pdf.ln(10)
        
        # Encabezado de la tabla de productos
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(120, 10, "Item")
        pdf.cell(40, 10, "Precio", ln=True)
        
        # Listado de productos
        pdf.set_font("Arial", size=12)
        for item in pedido.items_comprados:
            pdf.cell(120, 10, item['item'])
            pdf.cell(40, 10, f"${item['precio']:.2f}", ln=True)
            
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        # Resumen de cobros (Incluyendo el Decorator del 5%)
        cargo_servicio = pedido.total * 0.05
        total_final = pedido.total + cargo_servicio

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(120, 10, "Subtotal (Platos):")
        pdf.cell(40, 10, f"${pedido.total:.2f}", ln=True)
        
        pdf.cell(120, 10, "Cargo por servicio App (5%):")
        pdf.cell(40, 10, f"${cargo_servicio:.2f}", ln=True)
        
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(120, 10, "TOTAL PAGADO:")
        pdf.cell(40, 10, f"${total_final:.2f}", ln=True)
        
        # Guardar archivo
        nombre_archivo = f"Boleta_Pedido_{pedido.id}_{pedido.cliente.nombre.replace(' ', '_')}.pdf"
        pdf.output(nombre_archivo)
        print(f"[*] Boleta PDF generada exitosamente: {nombre_archivo}")