import tkinter as tk

from backend.logica_negocio import GestorPedidos
from backend.usuarios import UsuarioFactory

from frontend.login import VentanaLogin
from frontend.app_admin import AdminApp
from frontend.app_cliente import ClienteApp
from frontend.app_restaurante import RestauranteApp
from frontend.app_repartidor import RepartidorApp

class SistemaEnrutador:
    def __init__(self, root):
        self.root = root
        self.root.withdraw() 
        
        self.gestor = GestorPedidos()
        
        if not any(u.nombre == "admin" for u in self.gestor.usuarios_registrados):
            admin = UsuarioFactory.crear_usuario(
                "Cliente", id=0, nombre="admin", email="admin@delivery.com",
                direccion="Admin", contraseña="1234"
            )
            self.gestor.registrar_usuario_sistema(admin)
            
        self._mostrar_login()

    def _mostrar_login(self):
        """Limpia la ventana y lanza el login."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.withdraw()
        VentanaLogin(self.root,self.gestor, self._iniciar_sesion)
        
    def cerrar_sesion(self):
        """Callback que fuerza el guardado y vuelve a la pantalla inicial."""
        self.gestor.guardar_datos_json()
        self.gestor.guardar_historial_json()
        print("[-] Sesión cerrada correctamente.")
        self._mostrar_login()

    def _iniciar_sesion(self, rol: str, nombre_usuario: str):
        usuario_actual = next((u for u in self.gestor.usuarios_registrados if u.nombre == nombre_usuario), None)
        
        if not usuario_actual: return

        if nombre_usuario.lower() == "admin":
            AdminApp(self.root, self.gestor, self.cerrar_sesion)
        elif rol == "Cliente":
            ClienteApp(self.root, usuario_actual, self.gestor, self.cerrar_sesion)
        elif rol == "Restaurante":
            RestauranteApp(self.root, usuario_actual, self.gestor, self.cerrar_sesion)
        elif rol == "Repartidor":
            RepartidorApp(self.root, usuario_actual, self.gestor, self.cerrar_sesion)

        self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", root.quit)
    app = SistemaEnrutador(root)
    root.mainloop()