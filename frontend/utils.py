import tkinter as tk
import re

# ==========================================
# UTILIDADES DE VALIDACIÓN (Funcionalidad 20)
# ==========================================

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

class ConsolaRedirector:
    """Redirige el print estándar hacia un widget Text de Tkinter."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, mensaje):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, mensaje)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')

    def flush(self):
        pass