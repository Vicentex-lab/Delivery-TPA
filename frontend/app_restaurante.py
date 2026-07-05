import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from frontend.utils import validar_precio


class RestauranteApp:
    def __init__(self, root, restaurante, gestor, callback_logout):
        self.root = root
        self.restaurante = restaurante
        self.gestor = gestor
        self.callback_logout = callback_logout

        self.root.title(f"Sistema de Delivery - Cocina | {self.restaurante.nombre}")
        self.root.geometry("850x650")

        self._configurar_estilos()
        self._crear_interfaz()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background="#2B2B2B", foreground="#FFFFFF", font=('Helvetica', 10))
        self.root.configure(bg="#2B2B2B")
        style.configure('TNotebook.Tab', padding=[15, 5], font=('Helvetica', 10, 'bold'), background="#3C3F41", foreground="#FFFFFF", borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', "#FF6B35")])
        style.configure('TButton', padding=6, font=('Helvetica', 10, 'bold'), background="#3C3F41", foreground="#FFFFFF")
        style.configure('TLabelframe', background="#2B2B2B", foreground="#FF6B35")
        style.configure('TLabelframe.Label', font=('Helvetica', 11, 'bold'), background="#2B2B2B", foreground="#FF6B35")
        style.configure('Treeview', background="#333333", foreground="#FFFFFF", fieldbackground="#333333", rowheight=30)
        style.map('Treeview', background=[('selected', "#FF6B35")])

    def _crear_interfaz(self):
        header = ttk.Frame(self.root)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"👨‍🍳 Restaurante: {self.restaurante.nombre}", font=('Helvetica', 11, 'bold')).pack(side='left')
        ttk.Button(header, text="🚪 Cerrar Sesión", command=self.callback_logout).pack(side='right')

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)

        self.tab_pedidos = ttk.Frame(notebook)
        self.tab_menu = ttk.Frame(notebook)
        notebook.add(self.tab_pedidos, text=' 👨‍🍳 Gestión de Cocina')
        notebook.add(self.tab_menu, text=' 📋 Mi Menú')

        self._construir_tab_pedidos()
        self._construir_tab_menu()
        self._actualizar_tabla_menu()

    def _construir_tab_pedidos(self):
        frame_acciones = ttk.Frame(self.tab_pedidos)
        frame_acciones.pack(fill='x', padx=20, pady=(15, 0))
        ttk.Button(frame_acciones, text="🔄 Refrescar", command=self._actualizar_pedidos).pack(side='left', padx=5)
        ttk.Button(frame_acciones, text="❌ Rechazar", command=lambda: self._cambiar_estado("Rechazado")).pack(side='right', padx=5)
        ttk.Button(frame_acciones, text="✅ Listo para Entrega", command=lambda: self._cambiar_estado("Listo para Entrega")).pack(side='right', padx=5)
        ttk.Button(frame_acciones, text="🍳 Aceptar y Preparar", command=lambda: self._cambiar_estado("En Preparación")).pack(side='right', padx=5)

        frame_tabla = ttk.LabelFrame(self.tab_pedidos, text="Pedidos Entrantes", padding=10)
        frame_tabla.pack(fill='both', expand=True, padx=20, pady=10)
        self.tree_pedidos = ttk.Treeview(frame_tabla, columns=('ID', 'Cliente', 'Items', 'Estado'), show='headings', height=14)
        for c in ('ID', 'Cliente', 'Items', 'Estado'):
            self.tree_pedidos.heading(c, text=c)
            self.tree_pedidos.column(c, anchor='center' if c != 'Cliente' else 'w')
        self.tree_pedidos.pack(fill='both', expand=True)
        self._actualizar_pedidos()

    def _actualizar_pedidos(self):
        for i in self.tree_pedidos.get_children(): self.tree_pedidos.delete(i)
        for p in [p for p in self.gestor.historial_pedidos if p.restaurante.id == self.restaurante.id and p.estado in ["Confirmado", "En Preparación", "Listo para Entrega"]]:
            self.tree_pedidos.insert('', tk.END, values=(f"{p.id}", p.cliente.nombre, len(p.items_comprados), p.estado))

    def _cambiar_estado(self, estado):
        sel = self.tree_pedidos.selection()
        if not sel: return
        pedido = next((p for p in self.gestor.historial_pedidos if p.id == int(self.tree_pedidos.item(sel[0], 'values')[0])), None)
        
        if pedido:
            # 1. Validar que no rechace si ya está preparándolo o listo
            if estado == "Rechazado" and pedido.estado in ["En Preparación", "Listo para Entrega"]:
                messagebox.showerror("Acción Denegada", "No puedes rechazar un pedido que ya comenzaste a preparar o que ya está listo.")
                return
                
            # 2. Validar que la preparación siga un orden lógico
            if estado == "En Preparación" and pedido.estado != "Confirmado":
                messagebox.showerror("Error", "Solo puedes comenzar a preparar pedidos que estén recién 'Confirmados'.")
                return
                
            if estado == "Listo para Entrega" and pedido.estado != "En Preparación":
                messagebox.showerror("Error", "El pedido debe estar 'En Preparación' antes de marcarse como listo.")
                return

            # Si pasa las validaciones, cambiamos el estado y guardamos
            pedido.actualizarEstado(estado)
            self.gestor.guardar_historial_json()
            self._actualizar_pedidos()

    def _construir_tab_menu(self):
        # Frame superior para añadir
        frame_nuevo = ttk.LabelFrame(self.tab_menu, text="Añadir Nuevo Plato", padding=15)
        frame_nuevo.pack(fill='x', padx=20, pady=10)
        ttk.Label(frame_nuevo, text="Nombre:").pack(side='left', padx=5)
        self.entry_nuevo_nombre = ttk.Entry(frame_nuevo, width=20)
        self.entry_nuevo_nombre.pack(side='left', padx=5)
        ttk.Label(frame_nuevo, text="Precio:").pack(side='left', padx=5)
        self.entry_nuevo_precio = ttk.Entry(frame_nuevo, width=10)
        self.entry_nuevo_precio.pack(side='left', padx=5)
        ttk.Button(frame_nuevo, text="➕ Añadir", command=self._agregar_plato).pack(side='left', padx=15)

        # Frame de la tabla y acciones
        frame_lista = ttk.LabelFrame(self.tab_menu, text="Menú", padding=10)
        frame_lista.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Botones de edición
        frame_acciones_menu = ttk.Frame(frame_lista)
        frame_acciones_menu.pack(fill='x', pady=(0, 10))
        ttk.Button(frame_acciones_menu, text="✏️ Editar Plato", command=self._editar_plato).pack(side='left', padx=5)
        ttk.Button(frame_acciones_menu, text="🗑️ Eliminar Plato", command=self._eliminar_plato).pack(side='left', padx=5)

        # Tabla del menú
        self.tree_menu = ttk.Treeview(frame_lista, columns=('Plato', 'Precio'), show='headings')
        self.tree_menu.heading('Plato', text='Plato')
        self.tree_menu.heading('Precio', text='Precio')
        self.tree_menu.pack(fill='both', expand=True)

    def _actualizar_tabla_menu(self):
        for i in self.tree_menu.get_children(): self.tree_menu.delete(i)
        for item in self.restaurante.menu: self.tree_menu.insert('', tk.END, values=(item['item'], f"${item['precio']:.2f}"))

    def _agregar_plato(self):
        nom, pr_str = self.entry_nuevo_nombre.get().strip(), self.entry_nuevo_precio.get().strip()
        valido, precio = validar_precio(pr_str)
        if nom and valido:
            self.restaurante.menu.append({'item': nom, 'precio': precio})
            self.gestor.guardar_datos_json()
            self._actualizar_tabla_menu()
            self.entry_nuevo_nombre.delete(0, tk.END); self.entry_nuevo_precio.delete(0, tk.END)
            
    def _editar_plato(self):
        seleccion = self.tree_menu.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un plato de la tabla para editar.")
            return
            
        # Obtener datos del plato seleccionado
        item = self.tree_menu.item(seleccion[0])
        nombre_actual = item['values'][0]
        # Limpiamos el signo de dólar para que sea fácil de editar en el Entry
        precio_actual_str = str(item['values'][1]).replace('$', '').strip()

        # 1. Crear una ventana emergente personalizada
        ventana_edicion = tk.Toplevel(self.root)
        ventana_edicion.title("✏️ Editar Plato")
        ventana_edicion.geometry("300x220")
        ventana_edicion.configure(bg="#2B2B2B")
        ventana_edicion.grab_set() # Hace que no puedas tocar la ventana principal hasta cerrar esta

        # 2. Construir los inputs dentro de la ventana
        ttk.Label(ventana_edicion, text="Nombre del plato:").pack(pady=(15, 5))
        entry_nombre = ttk.Entry(ventana_edicion, width=25)
        entry_nombre.pack(padx=10)
        entry_nombre.insert(0, nombre_actual) # Pre-cargar el nombre actual

        ttk.Label(ventana_edicion, text="Precio:").pack(pady=(10, 5))
        entry_precio = ttk.Entry(ventana_edicion, width=15)
        entry_precio.pack(padx=10)
        entry_precio.insert(0, precio_actual_str) # Pre-cargar el precio actual

        # 3. Función interna para guardar los cambios al apretar el botón
        def guardar_cambios():
            nuevo_nombre = entry_nombre.get().strip()
            nuevo_precio_str = entry_precio.get().strip()
            
            if not nuevo_nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío.", parent=ventana_edicion)
                return
                
            valido, nuevo_precio = validar_precio(nuevo_precio_str)
            if valido:
                # Usar el nuevo método del backend
                self.restaurante.modificar_plato(nombre_actual, nuevo_nombre, nuevo_precio)
                
                # Guardar en JSON y actualizar tabla
                self.gestor.guardar_datos_json()
                self._actualizar_tabla_menu()
                
                # Cerrar ventana emergente
                ventana_edicion.destroy()
                messagebox.showinfo("Éxito", "Plato actualizado correctamente.")
            else:
                messagebox.showerror("Error", "El precio ingresado no es válido.", parent=ventana_edicion)

        # 4. Botón de guardar en la ventana emergente
        ttk.Button(ventana_edicion, text="💾 Guardar Cambios", command=guardar_cambios).pack(pady=20)
        
    def _eliminar_plato(self):
        seleccion = self.tree_menu.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un plato para eliminar.")
            return
            
        item = self.tree_menu.item(seleccion[0])
        nombre_plato = item['values'][0]
        
        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar '{nombre_plato}' del menú?")
        if confirmar:
            # Eliminar usando el método existente de la clase Restaurante
            self.restaurante.eliminar_plato(nombre_plato)
            self.gestor.guardar_datos_json()
            self._actualizar_tabla_menu()