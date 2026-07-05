import tkinter as tk
from tkinter import ttk, messagebox
import sys
from backend.usuarios import UsuarioFactory
from frontend.utils import ConsolaRedirector
from frontend.formularios import (FormularioCliente, FormularioRepartidor, FormularioRestaurante, FormularioEditarCliente, FormularioEditarRepartidor, FormularioEditarMenu)

class AdminApp:
    def __init__(self, root, gestor, callback_logout):
        self.root = root
        self.gestor = gestor
        self.callback_logout = callback_logout

        self.root.title("Sistema de Delivery - Panel Central")
        self.root.geometry("850x680")

        self.clientes = [u for u in self.gestor.usuarios_registrados if u.rol == "Cliente"]
        self.restaurantes = [u for u in self.gestor.usuarios_registrados if u.rol == "Restaurante"]
        self.repartidores = [u for u in self.gestor.usuarios_registrados if u.rol == "Repartidor"]

        self._configurar_estilos()
        self._crear_interfaz()
        sys.stdout = ConsolaRedirector(self.consola_text)

    # --- TODO EL CÓDIGO VISUAL DEL ADMIN QUEDA IGUAL, EXCEPTO _crear_interfaz ---
    def _crear_interfaz(self):
        header = ttk.Frame(self.root)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text="👑 Rol: Administrador del Sistema", font=('Helvetica', 11, 'bold')).pack(side='left')
        ttk.Button(header, text="🚪 Cerrar Sesión", command=self.callback_logout).pack(side='right')

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)

        self.tab_gestion = ttk.Frame(notebook)
        self.tab_historial = ttk.Frame(notebook)
        self.tab_consola = ttk.Frame(notebook)

        notebook.add(self.tab_gestion, text=' 👥 Gestión de Usuarios')
        notebook.add(self.tab_historial, text=' 🌐 Historial Global')
        notebook.add(self.tab_consola, text=' 🖥 Consola del Servidor')

        self._construir_tab_gestion()
        self._construir_tab_historial()
        self._construir_tab_consola()
        self._actualizar_treeview()
        self._actualizar_historial_global()

    # --- RESTO DEL CÓDIGO DE APP_ADMIN (Mismos métodos de tu anterior AdminApp) ---
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

    def _nuevo_id(self): return max((u.id for u in self.gestor.usuarios_registrados), default=0) + 1

    def _construir_tab_gestion(self):
        f_btn = ttk.LabelFrame(self.tab_gestion, text="Registrar", padding=15); f_btn.pack(fill='x', padx=20, pady=(15, 5))
        ttk.Button(f_btn, text="+ Cliente", command=lambda: FormularioCliente(self.root, self._g_cli)).pack(side='left', padx=10, expand=True)
        ttk.Button(f_btn, text="+ Restaurante", command=lambda: FormularioRestaurante(self.root, self._g_res)).pack(side='left', padx=10, expand=True)
        ttk.Button(f_btn, text="+ Repartidor", command=lambda: FormularioRepartidor(self.root, self._g_rep)).pack(side='left', padx=10, expand=True)

        f_tab = ttk.LabelFrame(self.tab_gestion, text="Usuarios Registrados", padding=10); f_tab.pack(fill='both', expand=True, padx=20, pady=(5, 15))
        self.tree_usuarios = ttk.Treeview(f_tab, columns=('ID', 'Nombre', 'Rol', 'Email'), show='headings', height=10)
        for c in ('ID', 'Nombre', 'Rol', 'Email'): self.tree_usuarios.heading(c, text=c)
        self.tree_usuarios.pack(fill='both', expand=True)

        f_acc = ttk.Frame(f_tab); f_acc.pack(fill='x', pady=10)
        ttk.Button(f_acc, text="✏ Editar", command=self._ed).pack(side='left', padx=10)
        ttk.Button(f_acc, text="🗑 Eliminar", command=self._el).pack(side='left', padx=10)

    def _actualizar_treeview(self):
        for i in self.tree_usuarios.get_children(): self.tree_usuarios.delete(i)
        for u in self.gestor.usuarios_registrados:
            if u.rol != "Admin" and u.nombre.lower() != "admin":
                self.tree_usuarios.insert("", tk.END, values=(u.id, u.nombre, u.rol, u.email))

    def _g_cli(self, n,e,d,c): self.gestor.registrar_usuario_sistema(UsuarioFactory.crear_usuario("Cliente", id=self._nuevo_id(), nombre=n, email=e, direccion=d, contraseña=c)); self._actualizar_treeview()
    def _g_res(self, n,e,m): self.gestor.registrar_usuario_sistema(UsuarioFactory.crear_usuario("Restaurante", id=self._nuevo_id(), nombre=n, email=e, menu=m, contraseña="1234")); self._actualizar_treeview()
    def _g_rep(self, n,e,v,c): self.gestor.registrar_usuario_sistema(UsuarioFactory.crear_usuario("Repartidor", id=self._nuevo_id(), nombre=n, email=e, vehiculo=v, contraseña=c)); self._actualizar_treeview()

    def _ed(self):
        sel = self.tree_usuarios.selection()
        if not sel: return
        u = next((u for u in self.gestor.usuarios_registrados if u.id == int(self.tree_usuarios.item(sel[0], 'values')[0])), None)
        if u.rol == 'Cliente': FormularioEditarCliente(self.root, u, self._actualizar_treeview)
        elif u.rol == 'Repartidor': FormularioEditarRepartidor(self.root, u, self._actualizar_treeview)
        elif u.rol == 'Restaurante': FormularioEditarMenu(self.root, u, self._actualizar_treeview)

    def _el(self):
        sel = self.tree_usuarios.selection()
        if sel and messagebox.askyesno("Confirmar", "¿Eliminar?"):
            if self.gestor.dar_baja_usuario_soft_delete(int(self.tree_usuarios.item(sel[0], 'values')[0])): self._actualizar_treeview()
            else: messagebox.showerror("Error", "Tiene pedidos en curso.")

    def _construir_tab_historial(self):
        f = ttk.LabelFrame(self.tab_historial, text="Todas las transacciones", padding=10); f.pack(fill='both', expand=True, padx=20, pady=15)
        self.tree_hist = ttk.Treeview(f, columns=('ID', 'Cli', 'Rest', 'Rep', 'Total', 'Est'), show='headings', height=14)
        for c in ('ID', 'Cli', 'Rest', 'Rep', 'Total', 'Est'): self.tree_hist.heading(c, text=c)
        self.tree_hist.pack(fill='both', expand=True)

    def _actualizar_historial_global(self):
        for i in self.tree_hist.get_children(): self.tree_hist.delete(i)
        for p in self.gestor.historial_pedidos:
            self.tree_hist.insert('', tk.END, values=(p.id, p.cliente.nombre, p.restaurante.nombre, p.repartidor.nombre if p.repartidor else "N/A", f"${p.total:.2f}", p.estado))

    def _construir_tab_consola(self):
        self.consola_text = tk.Text(self.tab_consola, bg="black", fg="#00FF00", font=('Courier', 10), state='disabled', wrap='word')
        self.consola_text.pack(fill='both', expand=True, padx=10, pady=10)