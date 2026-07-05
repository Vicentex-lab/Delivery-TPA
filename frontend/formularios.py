import tkinter as tk
from tkinter import ttk, messagebox
import re

from frontend.utils import validar_email, validar_contrasena, validar_precio, Tooltip
from backend.logica_negocio import GestorPedidos

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

        if not all([nombre, email, direccion, contrasena]):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.", parent=self.ventana)
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

        if not all([nombre, email, vehiculo, contrasena]):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.", parent=self.ventana)
            return

        self.repartidor.nombre = nombre
        self.repartidor.email = email
        self.repartidor.vehiculo = vehiculo
        self.repartidor.contraseña = contrasena
        print(f"[*] Repartidor '{nombre}' actualizado correctamente.")
        self.callback()
        self.ventana.destroy()

class FormularioEditarMenu:
    def __init__(self, parent, restaurante, callback):
        self.restaurante = restaurante
        self.callback = callback
        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"Editar Restaurante: {restaurante.nombre}")
        self.ventana.geometry("420x550")
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

        ttk.Separator(frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky='ew', pady=10)
        ttk.Label(frame, text="Añadir nuevo plato:", font=('Helvetica', 10, 'bold')).grid(row=4, column=0, columnspan=2)
        
        frame_nuevo = ttk.Frame(frame)
        frame_nuevo.grid(row=5, column=0, columnspan=2, pady=5)
        self.entry_nuevo_nombre = ttk.Entry(frame_nuevo, width=15)
        self.entry_nuevo_nombre.pack(side='left', padx=2)
        self.entry_nuevo_precio = ttk.Entry(frame_nuevo, width=8)
        self.entry_nuevo_precio.pack(side='left', padx=2)
        ttk.Button(frame_nuevo, text="➕", command=self._agregar_plato).pack(side='left', padx=5)

        columnas = ('Plato', 'Precio Actual')
        self.tree_menu = ttk.Treeview(frame, columns=columnas, show='headings', height=5)
        self.tree_menu.heading('Plato', text='Plato')
        self.tree_menu.heading('Precio Actual', text='Precio Actual')
        self.tree_menu.grid(row=6, column=0, columnspan=2, pady=10)
        
        for item in restaurante.menu:
            self.tree_menu.insert('', tk.END, values=(item['item'], f"${item['precio']:.2f}"))

        frame_editar = ttk.Frame(frame)
        frame_editar.grid(row=7, column=0, columnspan=2, pady=6)
        ttk.Label(frame_editar, text="Nuevo precio ($):").pack(side='left', padx=5)
        self.entry_precio = ttk.Entry(frame_editar, width=10)
        self.entry_precio.pack(side='left', padx=5)
        ttk.Button(frame_editar, text="Actualizar seleccionado", command=self._actualizar_precio).pack(side='left', padx=5)

        ttk.Button(frame, text="Guardar cambios finales", command=self._guardar).grid(row=8, column=0, columnspan=2, pady=15)

    def _agregar_plato(self):
        nombre = self.entry_nuevo_nombre.get().strip()
        precio_str = self.entry_nuevo_precio.get().strip()
        
        valido, precio = validar_precio(precio_str)
        if nombre and valido:
            self.restaurante.menu.append({'item': nombre, 'precio': precio})
            self.tree_menu.insert('', tk.END, values=(nombre, f"${precio:.2f}"))
            self.entry_nuevo_nombre.delete(0, tk.END)
            self.entry_nuevo_precio.delete(0, tk.END)
            print(f"[*] Plato {nombre} añadido al menú.")
        else:
            messagebox.showerror("Error", "Nombre inválido o precio incorrecto.")

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

        nombre_plato = self.tree_menu.item(seleccion[0], 'values')[0]
        self.restaurante.modificar_item(nombre_plato, nuevo_precio)
        GestorPedidos().guardar_datos_json()

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

        self.restaurante.nombre = nombre
        self.restaurante.email = email
        GestorPedidos().guardar_datos_json()
        print(f"[*] Restaurante '{nombre}' actualizado correctamente.")
        self.callback()
        self.ventana.destroy()