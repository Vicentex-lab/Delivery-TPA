import tkinter as tk
from tkinter import ttk, messagebox
import re

from frontend.utils import validar_email, validar_contrasena, validar_precio, Tooltip
from backend.logica_negocio import GestorPedidos
from backend.usuarios import UsuarioFactory

# ==========================================
# FORMULARIOS CLIENTES Y REPARTIDORES
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

class FormularioRestaurante:
    def __init__(self, parent, callback_guardar):
        self.callback_guardar = callback_guardar
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Nuevo Restaurante")
        self.ventana.geometry("420x520")
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

        # --- CAMPO CONTRASEÑA CON ASTERISCOS ---
        ttk.Label(frame, text="Contraseña:").grid(row=3, column=0, sticky='e', padx=5, pady=4)
        self.entry_contrasena = ttk.Entry(frame, width=24, show="*")
        self.entry_contrasena.grid(row=3, column=1, pady=4)
        Tooltip(self.entry_contrasena, "Mínimo 6 caracteres, 1 Mayúscula y 1 Símbolo (!#@$%&*)")

        ttk.Separator(frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)
        
        ttk.Label(frame, text="Agregar platos al menú:", font=('Helvetica', 10, 'bold')).grid(row=5, column=0, columnspan=2)

        ttk.Label(frame, text="Plato:").grid(row=6, column=0, sticky='e', padx=5, pady=4)
        self.entry_plato = ttk.Entry(frame, width=24)
        self.entry_plato.grid(row=6, column=1, pady=4)

        ttk.Label(frame, text="Precio ($):").grid(row=7, column=0, sticky='e', padx=5, pady=4)
        self.entry_precio = ttk.Entry(frame, width=24)
        self.entry_precio.grid(row=7, column=1, pady=4)

        ttk.Button(frame, text="+ Añadir plato", command=self._agregar_plato).grid(row=8, column=0, columnspan=2, pady=4)

        self.lista_platos = tk.Listbox(frame, height=5, width=38)
        self.lista_platos.grid(row=9, column=0, columnspan=2, pady=4)

        ttk.Button(frame, text="💾 Registrar Restaurante", command=self._guardar).grid(row=10, column=0, columnspan=2, pady=10)

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
            messagebox.showwarning("Precio bajo", f"El precio ${precio} CLP es inferior a $1.000 CLP.\nSe recomiendan precios iguales o superiores al valor sugerido.", parent=self.ventana)

        self.platos_temp.append({'item': plato, 'precio': precio})
        self.lista_platos.insert(tk.END, f"{plato} - ${precio}")
        self.entry_plato.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        # 1. Validar campos vacíos
        if not nombre or not email or not contrasena:
            messagebox.showwarning("Campos vacíos", "Nombre, email y contraseña son obligatorios.", parent=self.ventana)
            return
            
        # 2. Validar nombre
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre):
            messagebox.showerror("Nombre inválido", "El nombre solo puede contener letras.", parent=self.ventana)
            return
            
        # 3. Validar correo
        if not validar_email(email):
            messagebox.showerror("Email inválido", "El correo debe terminar en @gmail.com.", parent=self.ventana)
            return
            
        # 4. Validar contraseña (¡Aquí estaba el error!)
        valido_pass, msg_pass = validar_contrasena(contrasena)
        if not valido_pass:
            messagebox.showerror("Contraseña inválida", msg_pass, parent=self.ventana)
            return
            
        # 5. Validar menú
        if not self.platos_temp:
            messagebox.showwarning("Menú vacío", "Agrega al menos un plato al menú.", parent=self.ventana)
            return

        # 6. Ejecutar callback y cerrar
        self.callback_guardar(nombre, email, self.platos_temp, contrasena)
        self.ventana.destroy()

# ==========================================
# FORMULARIOS DE EDICIÓN
# ==========================================
class FormularioEditarCliente:
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

        ttk.Button(frame, text="Guardar cambios", command=self._guardar).grid(row=5, column=0, columnspan=2, pady=12)

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        direccion = self.entry_direccion.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not nombre or not email or not direccion or not contrasena:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.", parent=self.ventana)
            return

        # --- VALIDACIONES NUEVAS ---
        if not validar_email(email):
            messagebox.showerror("Email inválido", "El correo debe ser una dirección válida de @gmail.com", parent=self.ventana)
            return

        valido_pass, msg_pass = validar_contrasena(contrasena)
        if not valido_pass:
            messagebox.showerror("Contraseña inválida", msg_pass, parent=self.ventana)
            return
        # ---------------------------

        self.cliente.nombre = nombre
        self.cliente.email = email
        self.cliente.direccionEntrega = direccion
        self.cliente.contraseña = contrasena
        GestorPedidos().guardar_datos_json()
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente.", parent=self.ventana)
        self.callback()
        self.ventana.destroy()

class FormularioEditarRepartidor:
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

        ttk.Label(frame, text="Vehículo:").grid(row=3, column=0, sticky='e', padx=5, pady=4)
        self.entry_vehiculo = ttk.Entry(frame, width=24)
        self.entry_vehiculo.insert(0, repartidor.vehiculo)
        self.entry_vehiculo.grid(row=3, column=1, pady=4)

        ttk.Label(frame, text="Contraseña:").grid(row=4, column=0, sticky='e', padx=5, pady=4)
        self.entry_contrasena = ttk.Entry(frame, width=24, show="*")
        self.entry_contrasena.insert(0, repartidor.contraseña)
        self.entry_contrasena.grid(row=4, column=1, pady=4)

        ttk.Button(frame, text="Guardar cambios", command=self._guardar).grid(row=5, column=0, columnspan=2, pady=12)

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        vehiculo = self.entry_vehiculo.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not nombre or not email or not vehiculo or not contrasena:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.", parent=self.ventana)
            return

        # --- VALIDACIONES NUEVAS ---
        if not validar_email(email):
            messagebox.showerror("Email inválido", "El correo debe ser una dirección válida de @gmail.com", parent=self.ventana)
            return

        valido_pass, msg_pass = validar_contrasena(contrasena)
        if not valido_pass:
            messagebox.showerror("Contraseña inválida", msg_pass, parent=self.ventana)
            return
        # ---------------------------

        self.repartidor.nombre = nombre
        self.repartidor.email = email
        self.repartidor.vehiculo = vehiculo
        self.repartidor.contraseña = contrasena
        GestorPedidos().guardar_datos_json()
        messagebox.showinfo("Éxito", "Repartidor actualizado correctamente.", parent=self.ventana)
        self.callback()
        self.ventana.destroy()

class FormularioEditarMenu:
    def __init__(self, parent, restaurante, callback):
        self.restaurante = restaurante
        self.callback = callback
        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"Gestionar - {restaurante.nombre}")
        self.ventana.geometry("550x500")
        self.ventana.grab_set()

        # Frame Datos Principales del Restaurante
        f_info = ttk.LabelFrame(self.ventana, text="Datos del Restaurante", padding=15)
        f_info.pack(fill='x', padx=15, pady=10)

        ttk.Label(f_info, text="Nombre:").grid(row=0, column=0, sticky='e', padx=5, pady=4)
        self.entry_nombre = ttk.Entry(f_info, width=25)
        self.entry_nombre.insert(0, restaurante.nombre)
        self.entry_nombre.grid(row=0, column=1, pady=4)

        ttk.Label(f_info, text="Email:").grid(row=1, column=0, sticky='e', padx=5, pady=4)
        self.entry_email = ttk.Entry(f_info, width=25)
        self.entry_email.insert(0, restaurante.email)
        self.entry_email.grid(row=1, column=1, pady=4)

        # NUEVO: Campo Contraseña para Restaurante
        ttk.Label(f_info, text="Contraseña:").grid(row=2, column=0, sticky='e', padx=5, pady=4)
        self.entry_contrasena = ttk.Entry(f_info, width=25)
        # Se añade control de errores por si algún restaurante viejo en el JSON no tiene contraseña asignada aún
        self.entry_contrasena.insert(0, getattr(restaurante, 'contraseña', '1234'))
        self.entry_contrasena.grid(row=2, column=1, pady=4)

        ttk.Button(f_info, text="💾 Guardar Datos", command=self._guardar).grid(row=3, column=0, columnspan=2, pady=10)

        # Frame Gestión de Platos (El resto de tu código del menú original se mantiene abajo)
        f_menu = ttk.LabelFrame(self.ventana, text="Menú de Platos", padding=15)
        f_menu.pack(fill='both', expand=True, padx=15, pady=10)

        f_add = ttk.Frame(f_menu)
        f_add.pack(fill='x', pady=5)
        ttk.Label(f_add, text="Plato:").pack(side='left')
        self.entry_plato = ttk.Entry(f_add, width=15)
        self.entry_plato.pack(side='left', padx=5)
        ttk.Label(f_add, text="Precio:").pack(side='left')
        self.entry_precio = ttk.Entry(f_add, width=8)
        self.entry_precio.pack(side='left', padx=5)
        ttk.Button(f_add, text="➕", command=self._añadir_plato).pack(side='left')
        ttk.Button(f_add, text="❌", command=self._eliminar_plato).pack(side='left')

        self.tree_menu = ttk.Treeview(f_menu, columns=('Plato', 'Precio'), show='headings', height=6)
        self.tree_menu.heading('Plato', text='Plato'); self.tree_menu.heading('Precio', text='Precio')
        self.tree_menu.pack(fill='both', expand=True, pady=5)

        for item in self.restaurante.menu:
            # Recordar usar enteros de acuerdo al cambio anterior sin .2f
            self.tree_menu.insert('', tk.END, values=(item['item'], f"${item['precio']}"))

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not nombre or not email or not contrasena:
            messagebox.showwarning("Campos vacíos", "Todos los campos del restaurante son obligatorios.", parent=self.ventana)
            return

        # --- VALIDACIONES NUEVAS ---
        if not validar_email(email):
            messagebox.showerror("Email inválido", "El correo debe ser una dirección válida de @gmail.com", parent=self.ventana)
            return

        valido_pass, msg_pass = validar_contrasena(contrasena)
        if not valido_pass:
            messagebox.showerror("Contraseña inválida", msg_pass, parent=self.ventana)
            return
        # ---------------------------

        self.restaurante.nombre = nombre
        self.restaurante.email = email
        self.restaurante.contraseña = contrasena
        GestorPedidos().guardar_datos_json()
        messagebox.showinfo("Éxito", "Datos del restaurante actualizados.", parent=self.ventana)
        self.callback()

    def _añadir_plato(self):
        plato = self.entry_plato.get().strip()
        precio_str = self.entry_precio.get().strip()
        if not plato or not precio_str: return
        valido, precio = validar_precio(precio_str)
        if valido:
            self.restaurante.menu.append({'item': plato, 'precio': precio})
            GestorPedidos().guardar_datos_json()
            self.tree_menu.insert('', tk.END, values=(plato, f"${precio}"))
            self.entry_plato.delete(0, tk.END); self.entry_precio.delete(0, tk.END)
            self.callback()
        else:
            messagebox.showerror("Error", "Precio inválido.", parent=self.ventana)

    def _eliminar_plato(self):
        sel = self.tree_menu.selection()
        if sel:
            nombre_plato = self.tree_menu.item(sel[0], 'values')[0]
            self.restaurante.menu = [p for p in self.restaurante.menu if p['item'] != nombre_plato]
            GestorPedidos().guardar_datos_json()
            self.tree_menu.delete(sel[0])
            self.callback()