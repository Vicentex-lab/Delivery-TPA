import tkinter as tk
from tkinter import ttk, messagebox
import sys

from backend.logica_negocio import GestorPedidos
from backend.usuarios import UsuarioFactory, Pedido
from backend.interfaces import PagoTarjeta, PagoPaypal, CargoServicioDecorator

from frontend.utils import ConsolaRedirector
from frontend.login import VentanaLogin
from frontend.formularios import (
    FormularioCliente, FormularioRepartidor, FormularioRestaurante,
    FormularioEditarCliente, FormularioEditarRepartidor, FormularioEditarMenu
)

class DeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Delivery - Panel de Control")
        self.root.geometry("850x650")
        self.root.withdraw()

        self.clientes = []
        self.restaurantes = []
        self.repartidores = []
        self.carrito = []

        self.gestor = GestorPedidos()

        # Admin por defecto si no hay otros usuarios
        if not any(u.nombre == "admin" for u in self.gestor.usuarios_registrados):
            usuario_prueba = UsuarioFactory.crear_usuario(
                "Cliente", id=0, nombre="admin", email="admin@gmail.com",
                direccion="Admin", contraseña="1234"
            )
            self.gestor.registrar_usuario_sistema(usuario_prueba)

        VentanaLogin(self.gestor, self._abrir_panel)

    def _abrir_panel(self, rol: str):
        self.root.deiconify()
        self._configurar_estilos()
        self._crear_interfaz()
        sys.stdout = ConsolaRedirector(self.consola_text)
        print(f"--- SISTEMA DE DELIVERY INICIADO --- Bienvenido, rol: {rol}")
        
        self.clientes = [u for u in self.gestor.usuarios_registrados if u.rol == "Cliente"]
        self.restaurantes = [u for u in self.gestor.usuarios_registrados if u.rol == "Restaurante"]
        self.repartidores = [u for u in self.gestor.usuarios_registrados if u.rol == "Repartidor"]
        
        if hasattr(self, 'combo_restaurantes'):
            self.combo_restaurantes['values'] = [r.nombre for r in self.restaurantes]

        self._actualizar_treeview()
        
    def _nuevo_id(self):
        if self.gestor.usuarios_registrados:
            return max(u.id for u in self.gestor.usuarios_registrados) + 1
        return 1

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TEntry', foreground='black', fieldbackground='white')

        BG_COLOR = "#2B2B2B"          
        FG_COLOR = "#FFFFFF"          
        ACCENT_COLOR = "#FF6B35"      
        BTN_BG = "#3C3F41"            
        TREE_BG = "#333333"           

        style.configure('.', background=BG_COLOR, foreground=FG_COLOR, font=('Helvetica', 10))
        self.root.configure(bg=BG_COLOR) 

        style.configure('TNotebook', background=BG_COLOR, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[15, 5], font=('Helvetica', 10, 'bold'), 
                        background=BTN_BG, foreground=FG_COLOR, borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', ACCENT_COLOR)], foreground=[('selected', '#FFFFFF')])

        style.configure('TButton', padding=6, font=('Helvetica', 10, 'bold'), 
                        background=BTN_BG, foreground=FG_COLOR, borderwidth=1, bordercolor=BG_COLOR)
        style.map('TButton', background=[('active', ACCENT_COLOR)], foreground=[('active', '#FFFFFF')])

        style.configure('TLabelframe', background=BG_COLOR, bordercolor=BTN_BG, borderwidth=2)
        style.configure('TLabelframe.Label', font=('Helvetica', 11, 'bold'), background=BG_COLOR, foreground=ACCENT_COLOR)
        
        style.configure('Treeview', background=TREE_BG, foreground=FG_COLOR, fieldbackground=TREE_BG, rowheight=30, borderwidth=0)
        style.configure('Treeview.Heading', background=BTN_BG, foreground=FG_COLOR, font=('Helvetica', 10, 'bold'), borderwidth=1)
        style.map('Treeview', background=[('selected', ACCENT_COLOR)])
        
        style.configure('TSeparator', background=BTN_BG)
        style.configure('TCombobox', fieldbackground='white', background=BTN_BG, foreground='black')
        style.map('TCombobox', fieldbackground=[('readonly', 'white')], foreground=[('readonly', 'black')])

    def _crear_interfaz(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.tab_gestion = ttk.Frame(notebook)
        self.tab_pedido = ttk.Frame(notebook)
        self.tab_historial = ttk.Frame(notebook)
        self.tab_consola = ttk.Frame(notebook)

        notebook.add(self.tab_gestion, text=' 1. Gestión (CRUD)')
        notebook.add(self.tab_pedido, text=' 2. Nuevo Pedido')
        notebook.add(self.tab_historial, text=' 3. Historial')
        notebook.add(self.tab_consola, text=' 4. Consola / Tracking')

        self._construir_tab_gestion()
        self._construir_tab_pedido()
        self._construir_tab_historial()
        self._construir_tab_consola()

    def _construir_tab_gestion(self):
        frame_botones = ttk.LabelFrame(self.tab_gestion, text="Registrar Nuevas Entidades", padding=15)
        frame_botones.pack(fill='x', padx=20, pady=(15, 5))

        ttk.Button(frame_botones, text="+ Registrar Cliente", command=self._abrir_form_cliente).pack(side='left', padx=10, expand=True)
        ttk.Button(frame_botones, text="+ Registrar Restaurante", command=self._abrir_form_restaurante).pack(side='left', padx=10, expand=True)
        ttk.Button(frame_botones, text="+ Registrar Repartidor", command=self._abrir_form_repartidor).pack(side='left', padx=10, expand=True)

        frame_tabla = ttk.LabelFrame(self.tab_gestion, text="Usuarios Registrados", padding=10)
        frame_tabla.pack(fill='both', expand=True, padx=20, pady=(5, 15))

        columnas = ('ID', 'Nombre', 'Rol', 'Email', 'Detalle')
        self.tree_usuarios = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=10)

        self.tree_usuarios.heading('ID', text='ID')
        self.tree_usuarios.heading('Nombre', text='Nombre')
        self.tree_usuarios.heading('Rol', text='Rol')
        self.tree_usuarios.heading('Email', text='Email')
        self.tree_usuarios.heading('Detalle', text='Detalle')

        self.tree_usuarios.column('ID', width=40, anchor='center')
        self.tree_usuarios.column('Nombre', width=120)
        self.tree_usuarios.column('Rol', width=100, anchor='center')
        self.tree_usuarios.column('Email', width=180)
        self.tree_usuarios.column('Detalle', width=220)

        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscrollcommand=scrollbar.set)
        
        self.tree_usuarios.pack(side='top', fill='both', expand=False) 
        scrollbar.pack(side='right', fill='y')

        frame_acciones = ttk.Frame(frame_tabla)
        frame_acciones.pack(side='top', fill='x', pady=10) 
        
        ttk.Button(frame_acciones, text="✏ Editar", command=self._abrir_form_edicion).pack(side='left', padx=10)
        ttk.Button(frame_acciones, text="🗑 Eliminar", command=self._eliminar_usuario).pack(side='left', padx=10)
        self.tree_usuarios.bind("<Double-1>", lambda e: self._abrir_form_edicion())
        
    def _actualizar_treeview(self):
        for i in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(i)
        for u in self.gestor.usuarios_registrados:
            if u.rol == "Admin" or u.nombre.lower() == "admin":
                continue 
            self.tree_usuarios.insert("", tk.END, values=(u.id, u.nombre, u.rol, u.email))

    def _abrir_form_cliente(self): FormularioCliente(self.root, self._guardar_cliente)
    def _abrir_form_restaurante(self): FormularioRestaurante(self.root, self._guardar_restaurante)
    def _abrir_form_repartidor(self): FormularioRepartidor(self.root, self._guardar_repartidor)

    def _abrir_form_edicion(self):
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un usuario de la tabla para editar.")
            return

        valores = self.tree_usuarios.item(seleccion[0], 'values')
        id_usuario = int(valores[0])
        rol = valores[2]

        if rol == 'Cliente':
            usuario = next((c for c in self.clientes if c.id == id_usuario), None)
            if usuario: FormularioEditarCliente(self.root, usuario, self._post_edicion)

        elif rol == 'Repartidor':
            usuario = next((r for r in self.repartidores if r.id == id_usuario), None)
            if usuario: FormularioEditarRepartidor(self.root, usuario, self._post_edicion)

        elif rol == 'Restaurante':
            usuario = next((r for r in self.restaurantes if r.id == id_usuario), None)
            if usuario: FormularioEditarMenu(self.root, usuario, self._post_edicion)

    def _post_edicion(self):
        self._actualizar_treeview()
        print("[*] Datos actualizados correctamente.")
        
    def _eliminar_usuario(self):
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un usuario de la tabla para eliminar.")
            return

        valores = self.tree_usuarios.item(seleccion[0], 'values')
        id_usuario = int(valores[0])
        nombre = valores[1]
        rol = valores[2]

        if not messagebox.askyesno("Confirmar", f"¿Seguro que deseas dar de baja a {nombre} ({rol}) del sistema?"):
            return

        exito = self.gestor.dar_baja_usuario_soft_delete(id_usuario)
        if exito:
            if rol == 'Cliente':
                self.clientes = [c for c in self.clientes if c.id != id_usuario]
            elif rol == 'Restaurante':
                self.restaurantes = [r for r in self.restaurantes if r.id != id_usuario]
                self.combo_restaurantes['values'] = [r.nombre for r in self.restaurantes] 
            elif rol == 'Repartidor':
                self.repartidores = [rep for rep in self.repartidores if rep.id != id_usuario]

            messagebox.showinfo("Éxito", f"El {rol.lower()} '{nombre}' ha sido eliminado exitosamente.")
            self._actualizar_treeview()
        else:
            messagebox.showerror("Error", f"No se puede eliminar a {nombre}: Tiene pedidos en curso o pendientes.")

    def _guardar_cliente(self, nombre, email, direccion, contrasena):
        cliente = UsuarioFactory.crear_usuario("Cliente", id=self._nuevo_id(), nombre=nombre, email=email, direccion=direccion, contraseña=contrasena)
        self.clientes.append(cliente)
        self.gestor.registrar_usuario_sistema(cliente)
        self._actualizar_treeview()  
        print(f"[*] Creado: {cliente.obtenerDatos()}")

    def _guardar_restaurante(self, nombre, email, menu):
        restaurante = UsuarioFactory.crear_usuario("Restaurante", id=self._nuevo_id(), nombre=nombre, email=email, menu=menu, contraseña="1234")
        self.restaurantes.append(restaurante)
        self.gestor.registrar_usuario_sistema(restaurante) 
        self.gestor.guardar_datos_json() 
        if hasattr(self, 'combo_restaurantes'):
            self.combo_restaurantes['values'] = [r.nombre for r in self.restaurantes]
        self._actualizar_treeview()
        print(f"[*] Creado y guardado Restaurante: {restaurante.obtenerDatos()}")

    def _guardar_repartidor(self, nombre, email, vehiculo, contrasena):
        repartidor = UsuarioFactory.crear_usuario("Repartidor", id=self._nuevo_id(), nombre=nombre, email=email, vehiculo=vehiculo, contraseña=contrasena)
        self.repartidores.append(repartidor)
        self.gestor.registrar_usuario_sistema(repartidor)
        self.gestor.guardar_datos_json() 
        self._actualizar_treeview()
        print(f"[*] Creado y guardado Repartidor: {repartidor.obtenerDatos()}")

    def _construir_tab_pedido(self):
        frame_rest = ttk.LabelFrame(self.tab_pedido, text="Selección de Restaurante", padding=10)
        frame_rest.pack(fill='x', padx=20, pady=10)

        self.combo_restaurantes = ttk.Combobox(frame_rest, state="readonly")
        self.combo_restaurantes.pack(side='left', padx=10)
        self.combo_restaurantes.bind("<<ComboboxSelected>>", self._cargar_menu)

        frame_menu = ttk.Frame(self.tab_pedido)
        frame_menu.pack(fill='both', expand=True, padx=20, pady=5)

        lbl_menu = ttk.LabelFrame(frame_menu, text="Menú Disponible", padding=10)
        lbl_menu.pack(side='left', fill='both', expand=True, padx=5)
        self.lista_menu = tk.Listbox(lbl_menu, height=8, bg="#333333", fg="#FFFFFF", selectbackground="#FF6B35", borderwidth=0, highlightthickness=1, highlightcolor="#FF6B35")
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

        ttk.Button(frame_pago, text="Pagar y Confirmar Pedido", command=self._procesar_pedido).pack(side='right', padx=10)

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
            messagebox.showwarning("Sin selección", "Selecciona un plato del menú primero.")
            return
        index = seleccion[0]
        nombre_rest = self.combo_restaurantes.get()
        restaurante = next((r for r in self.restaurantes if r.nombre == nombre_rest), None)
        if restaurante:
            item = restaurante.menu[index]
            self.carrito.append(item)
            self.lista_carrito.insert(tk.END, f"{item['item']} - ${item['precio']}")
            print(f"[+] Añadido al carrito: {item['item']} (${item['precio']})")

    def _eliminar_del_carrito(self):
        seleccion = self.lista_carrito.curselection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un ítem del carrito para eliminarlo.")
            return
        index = seleccion[0]
        nombre_item = self.carrito[index]['item']
        self.carrito.pop(index)
        self.lista_carrito.delete(index)
        print(f"[-] Eliminado del carrito: {nombre_item}")

    def _vaciar_carrito(self):
        if not self.carrito:
            messagebox.showinfo("Carrito vacío", "El carrito ya está vacío.")
            return
        self.carrito.clear()
        self.lista_carrito.delete(0, tk.END)
        print("[-] Carrito vaciado completamente.")

    def _procesar_pedido(self):
        if not self.clientes or not self.repartidores:
            messagebox.showwarning("Atención", "Debes registrar al menos un Cliente y un Repartidor.")
            return
        if not self.carrito:
            messagebox.showwarning("Atención", "El carrito está vacío.")
            return

        cliente = self.clientes[0]
        nombre_rest = self.combo_restaurantes.get()
        restaurante = next((r for r in self.restaurantes if r.nombre == nombre_rest), None)

        print("\n--- INICIANDO PROCESO DE COMPRA ---")
        cliente.realizarPedido()

        pedido = Pedido(id_pedido=self._nuevo_id(), cliente=cliente, restaurante=restaurante, items_comprados=list(self.carrito))
        total = pedido.calcularTotal()
        print(f"Total a pagar: ${total:.2f}")

        repartidor = next((r for r in self.repartidores if r.disponible), None)
        if repartidor:
            pedido.repartidor = repartidor
            repartidor.disponible = False
            print(f"Asignación Automática: Repartidor {repartidor.nombre} asignado.")
        else:
            print("No hay repartidores disponibles.")
            return

        metodo_base = PagoTarjeta() if self.combo_pago.get() == "Tarjeta de Crédito" else PagoPaypal()
        metodo_decorado = CargoServicioDecorator(metodo_base)
        
        self.gestor.configurar_metodo_pago(metodo_decorado)
        self.gestor.confirmarPedido(pedido, cliente)
        restaurante.prepararPedido(pedido)
        pedido.actualizarEstado("En Camino")
        repartidor.actualizarUbicacion()
        repartidor.completarEntrega(pedido)

        self.carrito.clear()
        self.lista_carrito.delete(0, tk.END)
        self._actualizar_historial(pedido)
        messagebox.showinfo("Éxito", "¡Pedido procesado con éxito! Revisa la consola.")

    def _construir_tab_historial(self):
        frame_tabla = ttk.LabelFrame(self.tab_historial, text="Pedidos Completados", padding=10)
        frame_tabla.pack(fill='both', expand=True, padx=20, pady=15)

        columnas = ('ID', 'Cliente', 'Restaurante', 'Repartidor', 'Total', 'Estado')
        self.tree_historial = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=14)

        self.tree_historial.heading('ID', text='ID Pedido')
        self.tree_historial.heading('Cliente', text='Cliente')
        self.tree_historial.heading('Restaurante', text='Restaurante')
        self.tree_historial.heading('Repartidor', text='Repartidor')
        self.tree_historial.heading('Total', text='Total')
        self.tree_historial.heading('Estado', text='Estado')

        self.tree_historial.column('ID', width=70, anchor='center')
        self.tree_historial.column('Cliente', width=130)
        self.tree_historial.column('Restaurante', width=130)
        self.tree_historial.column('Repartidor', width=120)
        self.tree_historial.column('Total', width=80, anchor='center')
        self.tree_historial.column('Estado', width=110, anchor='center')

        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tree_historial.yview)
        self.tree_historial.configure(yscrollcommand=scrollbar.set)
        self.tree_historial.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def _actualizar_historial(self, pedido):
        repartidor_nombre = pedido.repartidor.nombre if pedido.repartidor else "N/A"
        self.tree_historial.insert('', tk.END, values=(
            f"#{pedido.id}", pedido.cliente.nombre, pedido.restaurante.nombre,
            repartidor_nombre, f"${pedido.total:.2f}", pedido.estado
        ))

    def _construir_tab_consola(self):
        self.consola_text = tk.Text(self.tab_consola, bg="black", fg="#00FF00", font=('Courier', 10), state='disabled', wrap='word')
        scrollbar = ttk.Scrollbar(self.tab_consola, orient='vertical', command=self.consola_text.yview)
        self.consola_text.configure(yscrollcommand=scrollbar.set)
        self.consola_text.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)