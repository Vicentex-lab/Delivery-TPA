import tkinter as tk
from tkinter import ttk, messagebox
import sys

from backend.facade import SistemaDeliveryFacade


# ==========================================
# UTILIDADES DE VALIDACIÓN (Funcionalidad 20)
# ==========================================
import re

def validar_email(email: str) -> bool:
    """Solo acepta correos que terminen en @gmail.com"""
    return email.lower().endswith("@gmail.com") and len(email) > len("@gmail.com")

def validar_contrasena(contrasena: str) -> tuple[bool, str]:
    """
    Valida que la contraseña cumpla los 3 requisitos.
    Retorna (True, '') si es válida, o (False, mensaje_error) si no.
    """
    if len(contrasena) < 6:
        return False, "Debe tener al menos 6 caracteres."
    if not re.search(r'[A-Z]', contrasena):
        return False, "Debe tener al menos 1 letra mayúscula."
    if not re.search(r'[!#@$%&*]', contrasena):
        return False, "Debe tener al menos 1 carácter no alfanumérico (!#@$%&*)."
    return True, ""

def validar_precio(precio_str: str) -> tuple[bool, float]:
    """Valida que el precio sea un número positivo y distinto de cero."""
    try:
        precio = float(precio_str)
        if precio <= 0:
            return False, 0.0
        return True, precio
    except ValueError:
        return False, 0.0


class Tooltip:
    """Cuadro de diálogo que aparece al pasar el mouse sobre un widget."""
    def __init__(self, widget, texto: str):
        self.widget = widget
        self.texto = texto
        self.ventana_tip = None
        widget.bind("<Enter>", self._mostrar)
        widget.bind("<Leave>", self._ocultar)

    def _mostrar(self, event=None):
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25

        self.ventana_tip = tk.Toplevel(self.widget)
        self.ventana_tip.wm_overrideredirect(True)  # Sin bordes ni barra de título
        self.ventana_tip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.ventana_tip, text=self.texto, justify='left',
            background="#FFFFE0", relief='solid', borderwidth=1,
            font=('Helvetica', 9), padx=6, pady=4
        )
        label.pack()

    def _ocultar(self, event=None):
        if self.ventana_tip:
            self.ventana_tip.destroy()
            self.ventana_tip = None

# ==========================================
# FUNCIONALIDAD 1: VENTANA DE LOGIN
# ==========================================
class VentanaLogin:
    def __init__(self, gestor: GestorPedidos, callback_exito):
        self.gestor = gestor
        self.callback_exito = callback_exito

        self.ventana = tk.Toplevel()
        self.ventana.title("Iniciar Sesión")
        self.ventana.geometry("350x220")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()

        self._construir_formulario()

    def _construir_formulario(self):
        frame = ttk.Frame(self.ventana, padding=30)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Sistema de Delivery", font=('Helvetica', 13, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        ttk.Label(frame, text="Usuario:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_usuario = ttk.Entry(frame, width=22)
        self.entry_usuario.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Contraseña:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.entry_contrasena = ttk.Entry(frame, width=22, show="*")
        self.entry_contrasena.grid(row=2, column=1, pady=5)
        self.entry_contrasena.bind("<Return>", lambda e: self._intentar_login())

        btn_login = ttk.Button(frame, text="Ingresar", command=self._intentar_login)
        btn_login.grid(row=3, column=0, columnspan=2, pady=15)

    def _intentar_login(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not usuario or not contrasena:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa usuario y contraseña.", parent=self.ventana)
            return

        rol = self.gestor.validar_login(usuario, contrasena)

        if rol:
            self.ventana.destroy()
            self.callback_exito(rol)
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.", parent=self.ventana)
            self.entry_contrasena.delete(0, tk.END)


# ==========================================
# FUNCIONALIDADES 2 y 3: FORMULARIO CLIENTES Y REPARTIDORES
# ==========================================
class FormularioCliente:
    def __init__(self, parent, callback_guardar):
        self.callback_guardar = callback_guardar

        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Nuevo Cliente")
        self.ventana.geometry("360x300")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()

        frame = ttk.Frame(self.ventana, padding=25)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Registrar Cliente", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 12))

        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky='e', padx=5, pady=4)
        self.entry_nombre = ttk.Entry(frame, width=24)
        self.entry_nombre.grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky='e', padx=5, pady=4)
        self.entry_email = ttk.Entry(frame, width=24)
        self.entry_email.grid(row=2, column=1, pady=4)
        Tooltip(self.entry_email, "Solo se aceptan correos @gmail.com")

        ttk.Label(frame, text="Dirección:").grid(row=3, column=0, sticky='e', padx=5, pady=4)
        self.entry_direccion = ttk.Entry(frame, width=24)
        self.entry_direccion.grid(row=3, column=1, pady=4)

        ttk.Label(frame, text="Contraseña:").grid(row=4, column=0, sticky='e', padx=5, pady=4)
        self.entry_contrasena = ttk.Entry(frame, width=24, show="*")
        self.entry_contrasena.grid(row=4, column=1, pady=4)
        TOOLTIP_CONTRASENA = "Debe tener al menos 6 caracteres\nDebe tener al menos 1 letra mayúscula\nDebe tener al menos 1 carácter no alfanumérico (!#@$%&*)"
        Tooltip(self.entry_contrasena, TOOLTIP_CONTRASENA)

        ttk.Button(frame, text="Guardar Cliente", command=self._guardar).grid(row=5, column=0, columnspan=2, pady=12)

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        direccion = self.entry_direccion.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not all([nombre, email, direccion, contrasena]):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.", parent=self.ventana)
            return
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre):
            messagebox.showerror("Nombre inválido", "El nombre solo puede contener letras.", parent=self.ventana)
            return
        if not validar_email(email):
            messagebox.showerror("Email inválido", "El email debe terminar en @gmail.com.", parent=self.ventana)
            return
        valida, error = validar_contrasena(contrasena)
        if not valida:
            messagebox.showerror("Contraseña inválida", error, parent=self.ventana)
            return

        self.callback_guardar(nombre, email, direccion, contrasena)
        self.ventana.destroy()


class FormularioRepartidor:
    def __init__(self, parent, callback_guardar):
        self.callback_guardar = callback_guardar

        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Nuevo Repartidor")
        self.ventana.geometry("360x270")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()

        frame = ttk.Frame(self.ventana, padding=25)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Registrar Repartidor", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 12))

        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky='e', padx=5, pady=4)
        self.entry_nombre = ttk.Entry(frame, width=24)
        self.entry_nombre.grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky='e', padx=5, pady=4)
        self.entry_email = ttk.Entry(frame, width=24)
        self.entry_email.grid(row=2, column=1, pady=4)
        Tooltip(self.entry_email, "Solo se aceptan correos @gmail.com")

        ttk.Label(frame, text="Vehículo:").grid(row=3, column=0, sticky='e', padx=5, pady=4)
        self.entry_vehiculo = ttk.Entry(frame, width=24)
        self.entry_vehiculo.grid(row=3, column=1, pady=4)

        ttk.Label(frame, text="Contraseña:").grid(row=4, column=0, sticky='e', padx=5, pady=4)
        self.entry_contrasena = ttk.Entry(frame, width=24, show="*")
        self.entry_contrasena.grid(row=4, column=1, pady=4)
        TOOLTIP_CONTRASENA = "Debe tener al menos 6 caracteres\nDebe tener al menos 1 letra mayúscula\nDebe tener al menos 1 carácter no alfanumérico (!#@$%&*)"
        Tooltip(self.entry_contrasena, TOOLTIP_CONTRASENA)

        ttk.Button(frame, text="Guardar Repartidor", command=self._guardar).grid(row=5, column=0, columnspan=2, pady=12)

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        vehiculo = self.entry_vehiculo.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not all([nombre, email, vehiculo, contrasena]):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.", parent=self.ventana)
            return
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre):
            messagebox.showerror("Nombre inválido", "El nombre solo puede contener letras.", parent=self.ventana)
            return
        if not validar_email(email):
            messagebox.showerror("Email inválido", "El email debe terminar en @gmail.com.", parent=self.ventana)
            return
        valida, error = validar_contrasena(contrasena)
        if not valida:
            messagebox.showerror("Contraseña inválida", error, parent=self.ventana)
            return

        self.callback_guardar(nombre, email, vehiculo, contrasena)
        self.ventana.destroy()


# ==========================================
# FUNCIONALIDADES 3 y 4: FORMULARIO RESTAURANTE + MENÚ
# ==========================================
class FormularioRestaurante:
    def __init__(self, parent, callback_guardar):
        self.callback_guardar = callback_guardar

        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Nuevo Restaurante")
        self.ventana.geometry("420x440")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()

        self.platos_temp = []

        frame = ttk.Frame(self.ventana, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Registrar Restaurante", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky='e', padx=5, pady=4)
        self.entry_nombre = ttk.Entry(frame, width=24)
        self.entry_nombre.grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky='e', padx=5, pady=4)
        self.entry_email = ttk.Entry(frame, width=24)
        self.entry_email.grid(row=2, column=1, pady=4)
        Tooltip(self.entry_email, "Solo se aceptan correos @gmail.com")

        ttk.Separator(frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky='ew', pady=8)
        ttk.Label(frame, text="Agregar platos al menú:", font=('Helvetica', 10, 'bold')).grid(row=4, column=0, columnspan=2)

        ttk.Label(frame, text="Plato:").grid(row=5, column=0, sticky='e', padx=5, pady=4)
        self.entry_plato = ttk.Entry(frame, width=24)
        self.entry_plato.grid(row=5, column=1, pady=4)

        ttk.Label(frame, text="Precio ($):").grid(row=6, column=0, sticky='e', padx=5, pady=4)
        self.entry_precio = ttk.Entry(frame, width=24)
        self.entry_precio.grid(row=6, column=1, pady=4)
        Tooltip(self.entry_precio, "Solo se aceptan números positivos y distintos de cero")

        ttk.Button(frame, text="+ Añadir plato", command=self._agregar_plato).grid(row=7, column=0, columnspan=2, pady=4)

        self.lista_platos = tk.Listbox(frame, height=5, width=38)
        self.lista_platos.grid(row=8, column=0, columnspan=2, pady=4)

        ttk.Button(frame, text="Guardar Restaurante", command=self._guardar).grid(row=9, column=0, columnspan=2, pady=10)

    def _agregar_plato(self):
        nombre_rest = self.entry_nombre.get().strip()
        email_rest = self.entry_email.get().strip()
        plato = self.entry_plato.get().strip()
        precio_str = self.entry_precio.get().strip()

        if not nombre_rest or not email_rest:
            messagebox.showwarning("Datos incompletos", "Debes ingresar el nombre y email del restaurante antes de agregar platos.", parent=self.ventana)
            return

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre_rest):
            messagebox.showerror("Nombre inválido", "El nombre del restaurante solo puede contener letras.", parent=self.ventana)
            return

        if not validar_email(email_rest):
            messagebox.showerror("Email inválido", "El email debe terminar en @gmail.com.", parent=self.ventana)
            return

        if not plato or not precio_str:
            messagebox.showwarning("Campos vacíos", "Ingresa nombre y precio del plato.", parent=self.ventana)
            return

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', plato):
            messagebox.showerror("Nombre inválido", "El nombre del plato solo puede contener letras.", parent=self.ventana)
            return

        valido, precio = validar_precio(precio_str)
        if not valido:
            messagebox.showerror("Precio inválido", "El precio debe ser un número positivo y distinto de cero.", parent=self.ventana)
            return

        if precio < 1000:
            messagebox.showwarning("Precio bajo", f"El precio ${precio:.2f} CLP es inferior a $1.000 CLP.\nSe recomiendan precios iguales o superiores al valor sugerido.", parent=self.ventana)

        self.platos_temp.append({'item': plato, 'precio': precio})
        self.lista_platos.insert(tk.END, f"{plato} - ${precio:.2f}")
        self.entry_plato.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()

        if not nombre or not email:
            messagebox.showwarning("Campos vacíos", "Nombre y email son obligatorios.", parent=self.ventana)
            return
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre):
            messagebox.showerror("Nombre inválido", "El nombre solo puede contener letras.", parent=self.ventana)
            return
        if not validar_email(email):
            messagebox.showerror("Email inválido", "El email debe terminar en @gmail.com.", parent=self.ventana)
            return
        if not self.platos_temp:
            messagebox.showwarning("Menú vacío", "Agrega al menos un plato al menú.", parent=self.ventana)
            return

        self.callback_guardar(nombre, email, self.platos_temp)
        self.ventana.destroy()


class ConsolaRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, mensaje):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, mensaje)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')

    def flush(self):
        pass


class DeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Delivery - Panel de Control")
        self.root.geometry("850x650")
        self.root.withdraw()

        self.carrito = []
        self._id_counter = 1 
        
        # Instanciamos el FACADE
        self.facade = SistemaDeliveryFacade()

        # El login ahora usa el facade
        VentanaLogin(self.facade, self._abrir_panel)

    def _abrir_panel(self, rol: str):
        self.root.deiconify()
        self._configurar_estilos()
        self._crear_interfaz()
        sys.stdout = ConsolaRedirector(self.consola_text)
        print(f"--- SISTEMA DE DELIVERY INICIADO --- Bienvenido, rol: {rol}")

    def _nuevo_id(self):
        """Genera un ID único incremental para cada entidad creada."""
        self._id_counter += 1
        return self._id_counter

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', padding=[15, 5], font=('Helvetica', 10, 'bold'))
        style.configure('TButton', padding=6, font=('Helvetica', 10))
        style.configure('TLabelframe', font=('Helvetica', 11, 'bold'))

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

    # ==========================================
    # PESTAÑA 1: GESTIÓN CON FORMULARIOS REALES
    # ==========================================
    def _construir_tab_gestion(self):
        # Botones de registro
        frame_botones = ttk.LabelFrame(self.tab_gestion, text="Registrar Nuevas Entidades", padding=15)
        frame_botones.pack(fill='x', padx=20, pady=(15, 5))

        ttk.Button(frame_botones, text="+ Registrar Cliente", command=self._abrir_form_cliente).pack(side='left', padx=10, expand=True)
        ttk.Button(frame_botones, text="+ Registrar Restaurante", command=self._abrir_form_restaurante).pack(side='left', padx=10, expand=True)
        ttk.Button(frame_botones, text="+ Registrar Repartidor", command=self._abrir_form_repartidor).pack(side='left', padx=10, expand=True)

        # Treeview de usuarios registrados (Funcionalidad 7)
        frame_tabla = ttk.LabelFrame(self.tab_gestion, text="Usuarios Registrados", padding=10)
        frame_tabla.pack(fill='both', expand=True, padx=20, pady=(5, 15))

        columnas = ('ID', 'Nombre', 'Rol', 'Email', 'Detalle')
        self.tree_usuarios = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=10)

        # Configurar columnas
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
        self.tree_usuarios.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Botón editar y doble click para editar
        ttk.Button(frame_tabla, text="✏ Editar seleccionado", command=self._abrir_form_edicion).pack(pady=(8, 0))
        self.tree_usuarios.bind("<Double-1>", lambda e: self._abrir_form_edicion())

    def _actualizar_treeview(self):
        """Refresca la tabla con todos los usuarios registrados en tiempo real."""
        self.tree_usuarios.delete(*self.tree_usuarios.get_children())

        for c in self.facade.clientes:
            self.tree_usuarios.insert('', tk.END, values=(
                c.id, c.nombre, 'Cliente', c.email, f"Dir: {c.direccionEntrega}"
            ))
        for r in self.facade.restaurantes:
            self.tree_usuarios.insert('', tk.END, values=(
                r.id, r.nombre, 'Restaurante', r.email, f"{len(r.menu)} platos en menú"
            ))
        for rep in self.facade.repartidores:
            estado = "Disponible" if rep.disponible else "Ocupado"
            self.tree_usuarios.insert('', tk.END, values=(
                rep.id, rep.nombre, 'Repartidor', rep.email, f"{rep.vehiculo} | {estado}"
            ))

    def _abrir_form_cliente(self):
        FormularioCliente(self.root, self._guardar_cliente)
    
    def _abrir_form_edicion(self):
        """Detecta qué tipo de usuario está seleccionado y abre el formulario correspondiente."""
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un usuario de la tabla para editar.")
            return

        valores = self.tree_usuarios.item(seleccion[0], 'values')
        id_usuario = int(valores[0])
        rol = valores[2]

        if rol == 'Cliente':
            usuario = next((c for c in self.facade.clientes if c.id == id_usuario), None)
            if usuario:
                FormularioEditarCliente(self.root, usuario, self._post_edicion)

        elif rol == 'Repartidor':
            usuario = next((r for r in self.facade.repartidores if r.id == id_usuario), None)
            if usuario:
                FormularioEditarRepartidor(self.root, usuario, self._post_edicion)

        elif rol == 'Restaurante':
            usuario = next((r for r in self.facade.restaurantes if r.id == id_usuario), None)
            if usuario:
                FormularioEditarMenu(self.root, usuario, self._post_edicion)

    def _post_edicion(self):
        """Se llama después de cualquier edición para refrescar el Treeview."""
        self._actualizar_treeview()
        print("[*] Datos actualizados correctamente.")

    def _guardar_cliente(self, nombre, email, direccion, contrasena):
        cliente = UsuarioFactory.crear_usuario(
            "Cliente", id=self._nuevo_id(), nombre=nombre,
            email=email, direccion=direccion, contraseña=contrasena
        )
        self.facade.clientes.append(cliente)
        self.gestor.registrar_usuario_sistema(cliente)
        self._actualizar_treeview()  # Refresca la tabla automáticamente
        print(f"[*] Creado: {cliente.obtenerDatos()}")

    def _abrir_form_restaurante(self):
        FormularioRestaurante(self.root, self._guardar_restaurante)

    def _guardar_restaurante(self, nombre, email, menu):
        restaurante = UsuarioFactory.crear_usuario(
            "Restaurante", id=self._nuevo_id(), nombre=nombre,
            email=email, menu=menu
        )
        self.facade.restaurantes.append(restaurante)
        self.combo_restaurantes['values'] = [r.nombre for r in self.facade.restaurantes]
        self._actualizar_treeview()  # Refresca la tabla automáticamente
        print(f"[*] Creado: {restaurante.obtenerDatos()}")

    def _abrir_form_repartidor(self):
        FormularioRepartidor(self.root, self._guardar_repartidor)

    def _guardar_repartidor(self, nombre, email, vehiculo, contrasena):
        repartidor = UsuarioFactory.crear_usuario(
            "Repartidor", id=self._nuevo_id(), nombre=nombre,
            email=email, vehiculo=vehiculo, contraseña=contrasena
        )
        self.facade.repartidores.append(repartidor)
        self._actualizar_treeview()  # Refresca la tabla automáticamente
        print(f"[*] Creado: {repartidor.obtenerDatos()}")

    # ==========================================
    # PESTAÑA 2: NUEVO PEDIDO
    # ==========================================
    def _construir_tab_pedido(self):
        frame_rest = ttk.LabelFrame(self.tab_pedido, text="Selección de Restaurante", padding=10)
        frame_rest.pack(fill='x', padx=20, pady=10)

        self.combo_restaurantes = ttk.Combobox(frame_rest, state="readonly")
        self.combo_restaurantes.pack(side='left', padx=10)
        self.combo_restaurantes.bind("<<ComboboxSelected>>", self._cargar_menu)

        frame_menu = ttk.Frame(self.tab_pedido)
        frame_menu.pack(fill='both', expand=True, padx=20, pady=5)

        # Lista de Menú
        lbl_menu = ttk.LabelFrame(frame_menu, text="Menú Disponible", padding=10)
        lbl_menu.pack(side='left', fill='both', expand=True, padx=5)
        self.lista_menu = tk.Listbox(lbl_menu, height=8)
        self.lista_menu.pack(fill='both', expand=True)
        ttk.Button(lbl_menu, text="Añadir al Carrito ->", command=self._agregar_al_carrito).pack(pady=5)

        # Lista de Carrito con botones de eliminación (Funcionalidades 5 y 18)
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
        restaurante = next((r for r in self.facade.restaurantes if r.nombre == nombre_rest), None)
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
        restaurante = next((r for r in self.facade.restaurantes if r.nombre == nombre_rest), None)
        if restaurante:
            item = restaurante.menu[index]
            self.carrito.append(item)
            self.lista_carrito.insert(tk.END, f"{item['item']} - ${item['precio']}")
            print(f"[+] Añadido al carrito: {item['item']} (${item['precio']})")

    def _eliminar_del_carrito(self):
        """[Funcionalidad 18] Elimina el ítem seleccionado del carrito."""
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
        """Limpia todos los ítems del carrito de una vez."""
        if not self.carrito:
            messagebox.showinfo("Carrito vacío", "El carrito ya está vacío.")
            return
        self.carrito.clear()
        self.lista_carrito.delete(0, tk.END)
        print("[-] Carrito vaciado completamente.")

    def _procesar_pedido(self):
        if not self.facade.clientes or not self.facade.repartidores:
            messagebox.showwarning("Atención", "Debes registrar al menos un Cliente y un Repartidor.")
            return
        if not self.carrito:
            messagebox.showwarning("Atención", "El carrito está vacío.")
            return

        cliente = self.facade.clientes[0]
        nombre_rest = self.combo_restaurantes.get()
        restaurante = next((r for r in self.facade.restaurantes if r.nombre == nombre_rest), None)

        print("\n--- INICIANDO PROCESO DE COMPRA ---")
        cliente.realizarPedido()

        pedido = Pedido(id_pedido=self._nuevo_id(), cliente=cliente, restaurante=restaurante, items_comprados=list(self.carrito))
        total = pedido.calcularTotal()
        print(f"Total a pagar: ${total:.2f}")

        repartidor = next((r for r in self.facade.repartidores if r.disponible), None)
        if repartidor:
            pedido.repartidor = repartidor
            repartidor.disponible = False
            print(f"Asignación Automática: Repartidor {repartidor.nombre} asignado.")
        else:
            print("No hay repartidores disponibles.")
            return

        metodo = PagoTarjeta() if self.combo_pago.get() == "Tarjeta de Crédito" else PagoPaypal()
        self.gestor.configurar_metodo_pago(metodo)
        self.gestor.confirmarPedido(pedido, cliente)
        restaurante.prepararPedido(pedido)
        pedido.actualizarEstado("En Camino")
        repartidor.actualizarUbicacion()
        repartidor.completarEntrega(pedido)

        self.carrito.clear()
        self.lista_carrito.delete(0, tk.END)
        self._actualizar_historial(pedido)  # Registra en el historial
        messagebox.showinfo("Éxito", "¡Pedido procesado con éxito! Revisa la consola.")

    # ==========================================
    # PESTAÑA 3: HISTORIAL DE TRANSACCIONES
    # ==========================================
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
        """Agrega un pedido completado al Treeview de historial."""
        repartidor_nombre = pedido.repartidor.nombre if pedido.repartidor else "N/A"
        self.tree_historial.insert('', tk.END, values=(
            f"#{pedido.id}",
            pedido.cliente.nombre,
            pedido.restaurante.nombre,
            repartidor_nombre,
            f"${pedido.total:.2f}",
            pedido.estado
        ))

    # ==========================================
    # PESTAÑA 3: CONSOLA DE EVENTOS
    # ==========================================
    def _construir_tab_consola(self):
        self.consola_text = tk.Text(self.tab_consola, bg="black", fg="#00FF00", font=('Courier', 10), state='disabled', wrap='word')
        scrollbar = ttk.Scrollbar(self.tab_consola, orient='vertical', command=self.consola_text.yview)
        self.consola_text.configure(yscrollcommand=scrollbar.set)
        self.consola_text.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)

    # ==========================================
    # FUNCIONALIDADES 11 Y 12: FORMULARIOS DE EDICIÓN
    # ==========================================
class FormularioEditarCliente:
    """[Funcionalidad 11] Edita todos los datos de un cliente."""
    def __init__(self, parent, cliente, callback):
        self.cliente = cliente
        self.callback = callback

        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"Editar Cliente: {cliente.nombre}")
        self.ventana.geometry("360x280")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()

        frame = ttk.Frame(self.ventana, padding=25)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text=f"Editando: {cliente.nombre}", font=('Helvetica', 11, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 12))

        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky='e', padx=5, pady=4)
        self.entry_nombre = ttk.Entry(frame, width=24)
        self.entry_nombre.insert(0, cliente.nombre)
        self.entry_nombre.grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky='e', padx=5, pady=4)
        self.entry_email = ttk.Entry(frame, width=24)
        self.entry_email.insert(0, cliente.email)
        self.entry_email.grid(row=2, column=1, pady=4)
        Tooltip(self.entry_email, "Solo se aceptan correos @gmail.com")

        ttk.Label(frame, text="Dirección:").grid(row=3, column=0, sticky='e', padx=5, pady=4)
        self.entry_direccion = ttk.Entry(frame, width=24)
        self.entry_direccion.insert(0, cliente.direccionEntrega)
        self.entry_direccion.grid(row=3, column=1, pady=4)

        ttk.Label(frame, text="Contraseña:").grid(row=4, column=0, sticky='e', padx=5, pady=4)
        self.entry_contrasena = ttk.Entry(frame, width=24, show="*")
        self.entry_contrasena.insert(0, cliente.contraseña)
        self.entry_contrasena.grid(row=4, column=1, pady=4)
        Tooltip(self.entry_contrasena, "Debe tener al menos 6 caracteres\nDebe tener al menos 1 letra mayúscula\nDebe tener al menos 1 carácter no alfanumérico (!#@$%&*)")

        ttk.Button(frame, text="Guardar cambios", command=self._guardar).grid(row=5, column=0, columnspan=2, pady=12)

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        direccion = self.entry_direccion.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not all([nombre, email, direccion, contrasena]):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.", parent=self.ventana)
            return
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre):
            messagebox.showerror("Nombre inválido", "El nombre solo puede contener letras.", parent=self.ventana)
            return
        if not validar_email(email):
            messagebox.showerror("Email inválido", "El email debe terminar en @gmail.com.", parent=self.ventana)
            return
        valida, error = validar_contrasena(contrasena)
        if not valida:
            messagebox.showerror("Contraseña inválida", error, parent=self.ventana)
            return

        self.cliente.nombre = nombre
        self.cliente.email = email
        self.cliente.actualizar_direccion(direccion)
        self.cliente.contraseña = contrasena
        print(f"[*] Cliente '{nombre}' actualizado correctamente.")
        self.callback()
        self.ventana.destroy()


class FormularioEditarRepartidor:
    """[Funcionalidad 11] Edita todos los datos de un repartidor."""
    def __init__(self, parent, repartidor, callback):
        self.repartidor = repartidor
        self.callback = callback

        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"Editar Repartidor: {repartidor.nombre}")
        self.ventana.geometry("360x280")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()

        frame = ttk.Frame(self.ventana, padding=25)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text=f"Editando: {repartidor.nombre}", font=('Helvetica', 11, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 12))

        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky='e', padx=5, pady=4)
        self.entry_nombre = ttk.Entry(frame, width=24)
        self.entry_nombre.insert(0, repartidor.nombre)
        self.entry_nombre.grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky='e', padx=5, pady=4)
        self.entry_email = ttk.Entry(frame, width=24)
        self.entry_email.insert(0, repartidor.email)
        self.entry_email.grid(row=2, column=1, pady=4)
        Tooltip(self.entry_email, "Solo se aceptan correos @gmail.com")

        ttk.Label(frame, text="Vehículo:").grid(row=3, column=0, sticky='e', padx=5, pady=4)
        self.entry_vehiculo = ttk.Entry(frame, width=24)
        self.entry_vehiculo.insert(0, repartidor.vehiculo)
        self.entry_vehiculo.grid(row=3, column=1, pady=4)

        ttk.Label(frame, text="Contraseña:").grid(row=4, column=0, sticky='e', padx=5, pady=4)
        self.entry_contrasena = ttk.Entry(frame, width=24, show="*")
        self.entry_contrasena.insert(0, repartidor.contraseña)
        self.entry_contrasena.grid(row=4, column=1, pady=4)
        Tooltip(self.entry_contrasena, "Debe tener al menos 6 caracteres\nDebe tener al menos 1 letra mayúscula\nDebe tener al menos 1 carácter no alfanumérico (!#@$%&*)")

        ttk.Button(frame, text="Guardar cambios", command=self._guardar).grid(row=5, column=0, columnspan=2, pady=12)

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        vehiculo = self.entry_vehiculo.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not all([nombre, email, vehiculo, contrasena]):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.", parent=self.ventana)
            return
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre):
            messagebox.showerror("Nombre inválido", "El nombre solo puede contener letras.", parent=self.ventana)
            return
        if not validar_email(email):
            messagebox.showerror("Email inválido", "El email debe terminar en @gmail.com.", parent=self.ventana)
            return
        valida, error = validar_contrasena(contrasena)
        if not valida:
            messagebox.showerror("Contraseña inválida", error, parent=self.ventana)
            return

        self.repartidor.nombre = nombre
        self.repartidor.email = email
        self.repartidor.vehiculo = vehiculo
        self.repartidor.contraseña = contrasena
        print(f"[*] Repartidor '{nombre}' actualizado correctamente.")
        self.callback()
        self.ventana.destroy()


class FormularioEditarMenu:
    """[Funcionalidad 12] Edita nombre, email y precios del menú de un restaurante."""
    def __init__(self, parent, restaurante, callback):
        self.restaurante = restaurante
        self.callback = callback

        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"Editar Restaurante: {restaurante.nombre}")
        self.ventana.geometry("420x450")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()

        frame = ttk.Frame(self.ventana, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text=f"Editando: {restaurante.nombre}", font=('Helvetica', 11, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky='e', padx=5, pady=4)
        self.entry_nombre = ttk.Entry(frame, width=24)
        self.entry_nombre.insert(0, restaurante.nombre)
        self.entry_nombre.grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky='e', padx=5, pady=4)
        self.entry_email = ttk.Entry(frame, width=24)
        self.entry_email.insert(0, restaurante.email)
        self.entry_email.grid(row=2, column=1, pady=4)
        Tooltip(self.entry_email, "Solo se aceptan correos @gmail.com")

        ttk.Separator(frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky='ew', pady=8)
        ttk.Label(frame, text="Editar precio de plato:", font=('Helvetica', 10, 'bold')).grid(row=4, column=0, columnspan=2)

        columnas = ('Plato', 'Precio Actual')
        self.tree_menu = ttk.Treeview(frame, columns=columnas, show='headings', height=5)
        self.tree_menu.heading('Plato', text='Plato')
        self.tree_menu.heading('Precio Actual', text='Precio Actual')
        self.tree_menu.column('Plato', width=200)
        self.tree_menu.column('Precio Actual', width=110, anchor='center')
        self.tree_menu.grid(row=5, column=0, columnspan=2, pady=4)

        for item in restaurante.menu:
            self.tree_menu.insert('', tk.END, values=(item['item'], f"${item['precio']:.2f}"))

        frame_editar = ttk.Frame(frame)
        frame_editar.grid(row=6, column=0, columnspan=2, pady=6)

        ttk.Label(frame_editar, text="Nuevo precio ($):").pack(side='left', padx=5)
        self.entry_precio = ttk.Entry(frame_editar, width=12)
        self.entry_precio.pack(side='left', padx=5)
        Tooltip(self.entry_precio, "Solo se aceptan números positivos y distintos de cero")
        ttk.Button(frame_editar, text="Actualizar precio", command=self._actualizar_precio).pack(side='left', padx=5)

        ttk.Button(frame, text="Guardar cambios", command=self._guardar).grid(row=7, column=0, columnspan=2, pady=10)

    def _actualizar_precio(self):
        seleccion = self.tree_menu.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un plato de la lista.", parent=self.ventana)
            return

        precio_str = self.entry_precio.get().strip()
        valido, nuevo_precio = validar_precio(precio_str)
        if not valido:
            messagebox.showerror("Precio inválido", "El precio debe ser un número positivo y distinto de cero.", parent=self.ventana)
            return

        if nuevo_precio < 1000:
            messagebox.showwarning(
                "Precio bajo",
                f"El precio ${nuevo_precio:.2f} CLP es inferior a $1.000 CLP.\nSe recomiendan precios iguales o superiores al valor sugerido.",
                parent=self.ventana
            )

        nombre_plato = self.tree_menu.item(seleccion[0], 'values')[0]
        self.restaurante.modificar_item(nombre_plato, nuevo_precio)

        self.tree_menu.delete(*self.tree_menu.get_children())
        for item in self.restaurante.menu:
            self.tree_menu.insert('', tk.END, values=(item['item'], f"${item['precio']:.2f}"))

        self.entry_precio.delete(0, tk.END)
        self.callback()

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()

        if not nombre or not email:
            messagebox.showwarning("Campos vacíos", "Nombre y email son obligatorios.", parent=self.ventana)
            return
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre):
            messagebox.showerror("Nombre inválido", "El nombre solo puede contener letras.", parent=self.ventana)
            return
        if not validar_email(email):
            messagebox.showerror("Email inválido", "El email debe terminar en @gmail.com.", parent=self.ventana)
            return

        self.restaurante.nombre = nombre
        self.restaurante.email = email
        print(f"[*] Restaurante '{nombre}' actualizado correctamente.")
        self.callback()
        self.ventana.destroy()    


if __name__ == "__main__":
    root = tk.Tk()
    app = DeliveryApp(root)
    root.mainloop()
