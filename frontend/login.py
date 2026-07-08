import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# FUNCIONALIDAD 1: VENTANA DE LOGIN
# ==========================================
class VentanaLogin:
    def __init__(self, parent, gestor, callback_exito): # Recibe parent (root)
        self.parent = parent
        self.gestor = gestor
        self.callback_exito = callback_exito

        self.ventana = tk.Toplevel(self.parent) # Se ancla al parent
        self.ventana.title("Iniciar Sesión")
        self.ventana.geometry("350x220")
        self.ventana.resizable(False, False)
        
        # Truco para evitar que se pierda el foco del teclado al cerrar sesión
        #self.ventana.transient(self.parent) 
        #self.ventana.grab_set()

        self._construir_formulario()

    def _construir_formulario(self):
        frame = ttk.Frame(self.ventana, padding=30)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Sistema de Delivery", font=('Helvetica', 13, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        ttk.Label(frame, text="Usuario:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_usuario = ttk.Entry(frame, width=22)
        self.entry_usuario.grid(row=1, column=1, pady=5)
        
        # Forzamos el cursor en el input de usuario
        self.entry_usuario.focus_force()

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
            self.callback_exito(rol, usuario)
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.", parent=self.ventana)
            self.entry_contrasena.delete(0, tk.END)
            self.entry_usuario.focus_force()