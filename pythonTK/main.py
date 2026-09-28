import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# GESTIÓN DE BASE DE DATOS
# ==========================================
class BaseDatos:
    def __init__(self, db_name="repair_center.db"):
        self.db_name = db_name
        self.inicializar_tablas()

    def obtener_conexion(self):
        return sqlite3.connect(self.db_name)

    def inicializar_tablas(self):
        with self.obtener_conexion() as conn:
            cursor = conn.cursor()
            
            # Tabla Usuarios para Login (Punto 3.3)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                clave TEXT NOT NULL
            )
            """)

            # Tabla Pedidos de Servicio Técnico (Punto 3.2)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                direccion TEXT NOT NULL,
                inconveniente TEXT NOT NULL,
                tecnico TEXT NOT NULL,
                fecha_visita TEXT NOT NULL
            )
            """)

            # Usuario inicial por defecto
            cursor.execute("INSERT OR IGNORE INTO usuarios (usuario, clave) VALUES (?, ?)", ("admin", "admin123"))
            conn.commit()

    def validar_usuario(self, usuario, clave):
        with self.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND clave = ?", (usuario, clave))
            return cursor.fetchone() is not None

    def guardar_pedido(self, cliente, direccion, inconveniente, tecnico, fecha_visita):
        with self.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pedidos (cliente, direccion, inconveniente, tecnico, fecha_visita)
                VALUES (?, ?, ?, ?, ?)
            """, (cliente, direccion, inconveniente, tecnico, fecha_visita))
            conn.commit()

    def obtener_pedidos(self):
        with self.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
            return cursor.fetchall()

    def eliminar_pedido(self, pedido_id):
        with self.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
            conn.commit()


# ==========================================
# VENTANA DE LOGIN (Punto 3.3)
# ==========================================
class VentanaLogin(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("Repair Center - Autenticación")
        self.geometry("350x220")
        self.resizable(False, False)

        # Centrar Ventana
        self.eval('tk::PlaceWindow . center')

        self._crear_widgets()

    def _crear_widgets(self):
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Acceso al Sistema", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        ttk.Label(frame, text="Usuario:").grid(row=1, column=0, sticky="e", pady=5)
        self.txt_usuario = ttk.Entry(frame)
        self.txt_usuario.grid(row=1, column=1, sticky="we", pady=5)
        self.txt_usuario.insert(0, "admin")  # Usuario demo

        ttk.Label(frame, text="Contraseña:").grid(row=2, column=0, sticky="e", pady=5)
        self.txt_clave = ttk.Entry(frame, show="*")
        self.txt_clave.grid(row=2, column=1, sticky="we", pady=5)
        self.txt_clave.insert(0, "admin123")  # Clave demo

        btn_ingresar = ttk.Button(frame, text="Ingresar", command=self._login)
        btn_ingresar.grid(row=3, column=0, columnspan=2, pady=(15, 0))

        frame.columnconfigure(1, weight=1)

    def _login(self):
        usr = self.txt_usuario.get().strip()
        pwd = self.txt_clave.get().strip()

        if self.db.validar_usuario(usr, pwd):
            self.destroy()  # Cierra la ventana de login
            app = VentanaPrincipal(self.db)
            app.mainloop()
        else:
            messagebox.showerror("Error de autenticación", "Usuario o contraseña incorrectos.")


# ==========================================
# VENTANA PRINCIPAL DE GESTIÓN (Punto 3.2)
# ==========================================
class VentanaPrincipal(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("Repair Center - Administración de Pedidos")
        self.geometry("850x550")

        self._crear_widgets()
        self._cargar_pedidos()

    def _crear_widgets(self):
        # Layout principal dividido en Formulario (Izquierda) y Tabla (Derecha)
        contenedor_formulario = ttk.LabelFrame(self, text=" Agendar Pedido de Servicio ", padding="15")
        contenedor_formulario.pack(side="left", fill="y", padx=10, pady=10)

        contenedor_tabla = ttk.Frame(self, padding="10")
        contenedor_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Campos de entrada
        ttk.Label(contenedor_formulario, text="Apellido y Nombre:").grid(row=0, column=0, sticky="w", pady=2)
        self.txt_cliente = ttk.Entry(contenedor_formulario, width=30)
        self.txt_cliente.grid(row=1, column=0, pady=(0, 8), sticky="we")

        ttk.Label(contenedor_formulario, text="Dirección (Calle y Altura):").grid(row=2, column=0, sticky="w", pady=2)
        self.txt_direccion = ttk.Entry(contenedor_formulario, width=30)
        self.txt_direccion.grid(row=3, column=0, pady=(0, 8), sticky="we")

        ttk.Label(contenedor_formulario, text="Inconveniente:").grid(row=4, column=0, sticky="w", pady=2)
        self.txt_inconveniente = tk.Text(contenedor_formulario, width=30, height=4)
        self.txt_inconveniente.grid(row=5, column=0, pady=(0, 8), sticky="we")

        ttk.Label(contenedor_formulario, text="Técnico Asignado:").grid(row=6, column=0, sticky="w", pady=2)
        self.cb_tecnico = ttk.Combobox(contenedor_formulario, values=[
            "Carlos Gómez", "Mariana López", "Roberto Sánchez", "Soporte General"
        ], state="readonly")
        self.cb_tecnico.grid(row=7, column=0, pady=(0, 8), sticky="we")
        self.cb_tecnico.current(0)

        ttk.Label(contenedor_formulario, text="Fecha y Hora (AAAA-MM-DD HH:MM):").grid(row=8, column=0, sticky="w", pady=2)
        self.txt_fecha = ttk.Entry(contenedor_formulario, width=30)
        self.txt_fecha.grid(row=9, column=0, pady=(0, 15), sticky="we")
        self.txt_fecha.insert(0, "2026-03-30 10:00")

        # Botones de Acción
        btn_guardar = ttk.Button(contenedor_formulario, text="Guardar Pedido", command=self._guardar)
        btn_guardar.grid(row=10, column=0, pady=5, sticky="we")

        btn_eliminar = ttk.Button(contenedor_formulario, text="Eliminar Seleccionado", command=self._eliminar)
        btn_eliminar.grid(row=11, column=0, pady=5, sticky="we")

        # Vista de árbol (Treeview) para mostrar la base de datos
        columnas = ("ID", "Cliente", "Dirección", "Inconveniente", "Técnico", "Fecha Visita")
        self.tabla = ttk.Treeview(contenedor_tabla, columns=columnas, show="headings")

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Dirección", text="Dirección")
        self.tabla.heading("Inconveniente", text="Inconveniente")
        self.tabla.heading("Técnico", text="Técnico")
        self.tabla.heading("Fecha Visita", text="Fecha/Hora")

        self.tabla.column("ID", width=30, anchor="center")
        self.tabla.column("Cliente", width=120)
        self.tabla.column("Dirección", width=120)
        self.tabla.column("Inconveniente", width=150)
        self.tabla.column("Técnico", width=100)
        self.tabla.column("Fecha Visita", width=110)

        scrollbar = ttk.Scrollbar(contenedor_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _guardar(self):
        cliente = self.txt_cliente.get().strip()
        direccion = self.txt_direccion.get().strip()
        inconveniente = self.txt_inconveniente.get("1.0", tk.END).strip()
        tecnico = self.cb_tecnico.get()
        fecha = self.txt_fecha.get().strip()

        if not (cliente and direccion and inconveniente and fecha):
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        self.db.guardar_pedido(cliente, direccion, inconveniente, tecnico, fecha)
        messagebox.showinfo("Éxito", "Pedido agendado correctamente.")
        self._limpiar_formulario()
        self._cargar_pedidos()

    def _cargar_pedidos(self):
        # Limpiar filas existentes en el Treeview
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # Cargar desde SQLite
        for registro in self.db.obtener_pedidos():
            self.tabla.insert("", "end", values=registro)

    def _eliminar(self):
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado:
            messagebox.showwarning("Atención", "Seleccione un pedido de la lista para eliminar.")
            return

        confirmacion = messagebox.askyesno("Confirmar", "¿Desea borrar el pedido seleccionado?")
        if confirmacion:
            pedido_id = self.tabla.item(item_seleccionado[0])['values'][0]
            self.db.eliminar_pedido(pedido_id)
            self._cargar_pedidos()

    def _limpiar_formulario(self):
        self.txt_cliente.delete(0, tk.END)
        self.txt_direccion.delete(0, tk.END)
        self.txt_inconveniente.delete("1.0", tk.END)
        self.txt_fecha.delete(0, tk.END)


# ==========================================
# PUNTO DE ENTRADA
# ==========================================
if __name__ == "__main__":
    base_datos = BaseDatos()
    login_app = VentanaLogin(base_datos)
    login_app.mainloop()