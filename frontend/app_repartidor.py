import tkinter as tk
from tkinter import ttk, messagebox

class RepartidorApp:
    def __init__(self, root, repartidor, gestor, callback_logout):
        self.root = root
        self.repartidor = repartidor
        self.gestor = gestor
        self.callback_logout = callback_logout

        self.root.title(f"Sistema de Delivery - Repartidor | {self.repartidor.nombre}")
        self.root.geometry("800x650")
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
        
        style.configure('TEntry', foreground="#000000", fieldbackground="#FFFFFF")
        
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
        ttk.Label(header, text=f"🛵 Repartidor: {self.repartidor.nombre} ({self.repartidor.vehiculo})", font=('Helvetica', 11, 'bold')).pack(side='left')
        ttk.Button(header, text="🚪 Cerrar Sesión", command=self.callback_logout).pack(side='right')

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tab_disp = ttk.Frame(notebook)
        self.tab_ruta = ttk.Frame(notebook)
        self.tab_historial = ttk.Frame(notebook) # Nueva pestaña

        notebook.add(self.tab_disp, text=' 🔔 Disponibles')
        notebook.add(self.tab_ruta, text=' 🛵 Mi Ruta')
        notebook.add(self.tab_historial, text=' 📜 Historial Entregas')

        self._construir_tab_disp()
        self._construir_tab_ruta()
        self._construir_tab_historial() # Nuevo constructor

    # --- PESTAÑA 1: DISPONIBLES ---
    def _construir_tab_disp(self):
        f_acc = ttk.Frame(self.tab_disp)
        f_acc.pack(fill='x', padx=20, pady=(15, 0))
        ttk.Button(f_acc, text="🔄 Refrescar", command=self._actualizar_disp).pack(side='left')
        ttk.Button(f_acc, text="📦 Tomar Pedido", command=self._tomar_pedido).pack(side='right')

        f_tabla = ttk.LabelFrame(self.tab_disp, text="Listos para Retirar", padding=10)
        f_tabla.pack(fill='both', expand=True, padx=20, pady=10)
        self.tree_disp = ttk.Treeview(f_tabla, columns=('ID', 'Rest', 'Destino'), show='headings')
        for c in ('ID', 'Rest', 'Destino'): self.tree_disp.heading(c, text=c)
        self.tree_disp.pack(fill='both', expand=True)
        self._actualizar_disp()

    def _actualizar_disp(self):
        for i in self.tree_disp.get_children(): self.tree_disp.delete(i)
        for p in [p for p in self.gestor.historial_pedidos if p.estado == "Listo para Entrega" and p.repartidor is None]:
            self.tree_disp.insert('', tk.END, values=(p.id, p.restaurante.nombre, p.cliente.direccionEntrega))

    def _tomar_pedido(self):
        if not self.repartidor.disponible:
            messagebox.showerror("Error", "Tienes un pedido en curso.")
            return
        sel = self.tree_disp.selection()
        if not sel: return
        pedido = next((p for p in self.gestor.historial_pedidos if p.id == int(self.tree_disp.item(sel[0], 'values')[0])), None)
        if pedido:
            pedido.repartidor = self.repartidor
            pedido.actualizarEstado("En Camino")
            self.gestor.guardar_datos_json() 
            self.gestor.guardar_historial_json()
            self._actualizar_disp()
            self._actualizar_ruta()

    # --- PESTAÑA 2: MI RUTA ---
    def _construir_tab_ruta(self):
        f_acc = ttk.Frame(self.tab_ruta)
        f_acc.pack(fill='x', padx=20, pady=(15, 0))
        ttk.Button(f_acc, text="🏁 Entregar", command=self._completar).pack(side='right')

        f_tabla = ttk.LabelFrame(self.tab_ruta, text="En Curso", padding=10)
        f_tabla.pack(fill='both', expand=True, padx=20, pady=10)
        self.tree_ruta = ttk.Treeview(f_tabla, columns=('ID', 'Cli', 'Dir', 'Est'), show='headings')
        for c in ('ID', 'Cli', 'Dir', 'Est'): self.tree_ruta.heading(c, text=c)
        self.tree_ruta.pack(fill='both', expand=True)
        self._actualizar_ruta()

    def _actualizar_ruta(self):
        for i in self.tree_ruta.get_children(): self.tree_ruta.delete(i)
        for p in [p for p in self.gestor.historial_pedidos if p.repartidor and p.repartidor.id == self.repartidor.id and p.estado == "En Camino"]:
            self.tree_ruta.insert('', tk.END, values=(p.id, p.cliente.nombre, p.cliente.direccionEntrega, p.estado))

    def _completar(self):
        sel = self.tree_ruta.selection()
        if not sel: return
        pedido = next((p for p in self.gestor.historial_pedidos if p.id == int(self.tree_ruta.item(sel[0], 'values')[0])), None)
        if pedido:
            self.repartidor.completarEntrega(pedido)
            self.gestor.guardar_datos_json()
            self.gestor.guardar_historial_json()
            self._actualizar_ruta()
            self._actualizar_disp()
            self._actualizar_historial() # Refresca el historial

    # --- PESTAÑA 3: HISTORIAL (NUEVA) ---
    def _construir_tab_historial(self):
        f_acc = ttk.Frame(self.tab_historial)
        f_acc.pack(fill='x', padx=20, pady=(15, 0))
        ttk.Button(f_acc, text="🔄 Refrescar", command=self._actualizar_historial).pack(side='left')

        f_tabla = ttk.LabelFrame(self.tab_historial, text="Mis Pedidos Entregados", padding=10)
        f_tabla.pack(fill='both', expand=True, padx=20, pady=10)
        self.tree_hist = ttk.Treeview(f_tabla, columns=('ID', 'Restaurante', 'Cliente', 'Total', 'Estado'), show='headings')
        
        for c in ('ID', 'Restaurante', 'Cliente', 'Total', 'Estado'): 
            self.tree_hist.heading(c, text=c)
            self.tree_hist.column(c, anchor='center' if c in ['ID', 'Total', 'Estado'] else 'w')

        self.tree_hist.pack(fill='both', expand=True)
        self._actualizar_historial()

    def _actualizar_historial(self):
        for i in self.tree_hist.get_children(): self.tree_hist.delete(i)
        # Filtramos solo los pedidos asignados a este repartidor y que estén completados (Entregados)
        entregados = [p for p in self.gestor.historial_pedidos if p.repartidor and p.repartidor.id == self.repartidor.id and p.estado == "Entregado"]
        for p in entregados:
            self.tree_hist.insert('', tk.END, values=(p.id, p.restaurante.nombre, p.cliente.nombre, f"${p.total}", p.estado))