import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# 1. GESTIÓN DE BASE DE DATOS (SQLite)
# ==========================================
class BaseDatosService:
    def __init__(self, db_name="repair_center.db"):
        self.db_name = db_name
        self._inicializar_tablas()

    def _obtener_conexion(self):
        return sqlite3.connect(self.db_name)

    def _inicializar_tablas(self):
        """Crea las tablas de usuarios y pedidos si no existen."""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            
            # Tabla para autenticación (Punto 3.3)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                clave TEXT NOT NULL
            )
            """)

            # Tabla para pedidos de servicio técnico (Punto 3.2)
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

            # Insertar un usuario por defecto si la tabla está vacía
            cursor.execute("INSERT OR IGNORE INTO usuarios (usuario, clave) VALUES (?, ?)", ("admin", "admin123"))
            conn.commit()

    def validar_credenciales(self, usuario, clave):
        """Valida si existe un registro con la combinación usuario/clave dada."""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND clave = ?", (usuario, clave))
            return cursor.fetchone() is not None

    def guardar_pedido(self, cliente, direccion, inconveniente, tecnico, fecha_visita):
        """Guarda un pedido en la base de datos."""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pedidos (cliente, direccion, inconveniente, tecnico, fecha_visita)
                VALUES (?, ?, ?, ?, ?)
            """, (cliente, direccion, inconveniente, tecnico, fecha_visita))
            conn.commit()

    def obtener_todos_los_pedidos(self):
        """Devuelve todos los pedidos guardados."""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
            return cursor.fetchall()

    def eliminar_pedido(self, pedido_id):
        """Elimina un pedido por su ID."""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
            conn.commit()


# ==========================================
# 2. PANTALLA DE LOGIN (Punto 3.3)
# ==========================================
class VentanaLogin(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("Repair Center - Autenticación")
        self.geometry("380x240")
        self.resizable(False, False)

        # Centrar la ventana en pantalla
        self.eval('tk::PlaceWindow . center')

        self._crear_interfaz()

    def _crear_interfaz(self):
        contenedor = ttk.Frame(self, padding="20")
        contenedor.pack(fill="both", expand=True)

        ttk.Label(contenedor, text="Inicio de Sesión", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Campo Usuario
        ttk.Label(contenedor, text="Usuario:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        self.txt_usuario = ttk.Entry(contenedor, width=25)
        self.txt_usuario.grid(row=1, column=1, sticky="w", pady=5)
        self.txt_usuario.insert(0, "admin")  # Usuario precargado para pruebas

        # Campo Contraseña
        ttk.Label(contenedor, text="Contraseña:").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.txt_clave = ttk.Entry(contenedor, show="*", width=25)
        self.txt_clave.grid(row=2, column=1, sticky="w", pady=5)
        self.txt_clave.insert(0, "admin123")  # Contraseña precargada para pruebas

        # Botón Ingresar
        btn_ingresar = ttk.Button(contenedor, text="Ingresar", command=self._autenticar)
        btn_ingresar.grid(row=3, column=0, columnspan=2, pady=(15, 0))

        # Permite confirmar el login al presionar la tecla Enter
        self.bind("<Return>", lambda e: self._autenticar())

    def _autenticar(self):
        usuario = self.txt_usuario.get().strip()
        clave = self.txt_clave.get().strip()

        if not usuario or not clave:
            messagebox.showwarning("Campos vacíos", "Por favor, ingrese usuario y contraseña.")
            return

        if self.db.validar_credenciales(usuario, clave):
            self.destroy()  # Cierra la ventana de login
            app = AppRepairCenter(self.db)  # Abre la aplicación principal
            app.mainloop()
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")


# ==========================================
# 3. INTERFAZ PRINCIPAL (Puntos 3.2.1 a 3.2.5)
# ==========================================
class AppRepairCenter(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("Repair Center - Administración de Pedidos")
        self.geometry("920x560")
        self.resizable(True, True)

        self._crear_interfaz()
        self._cargar_pedidos()

    def _crear_interfaz(self):
        # Panel Izquierdo: Formulario
        frame_form = ttk.LabelFrame(self, text=" Agendar Pedido de Servicio Técnico ", padding="15")
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        # Panel Derecho: Tabla de Pedidos
        frame_tabla = ttk.LabelFrame(self, text=" Historial de Pedidos Agendados ", padding="10")
        frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # ----------------------------------------------------
        # FORMULARIO DE INGRESO
        # ----------------------------------------------------
        # 3.2.1 Apellido y Nombre del Cliente
        ttk.Label(frame_form, text="3.2.1 Apellido y Nombre:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_cliente = ttk.Entry(frame_form, width=32)
        self.entry_cliente.grid(row=1, column=0, pady=(0, 8), sticky="we")

        # 3.2.2 Dirección
        ttk.Label(frame_form, text="3.2.2 Dirección (Calle y Altura):").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_direccion = ttk.Entry(frame_form, width=32)
        self.entry_direccion.grid(row=3, column=0, pady=(0, 8), sticky="we")

        # 3.2.3 Inconveniente
        ttk.Label(frame_form, text="3.2.3 Inconveniente reportado:").grid(row=4, column=0, sticky="w", pady=2)
        self.text_inconveniente = tk.Text(frame_form, width=32, height=4)
        self.text_inconveniente.grid(row=5, column=0, pady=(0, 8), sticky="we")

        # 3.2.4 Asignar un Técnico
        ttk.Label(frame_form, text="3.2.4 Asignar Técnico:").grid(row=6, column=0, sticky="w", pady=2)
        self.combo_tecnico = ttk.Combobox(frame_form, values=[
            "Carlos Gómez", "Mariana López", "Roberto Sánchez", "Soporte General"
        ], state="readonly")
        self.combo_tecnico.grid(row=7, column=0, pady=(0, 8), sticky="we")
        self.combo_tecnico.current(0)

        # 3.2.5 Agendar Visita (Fecha y Hora)
        ttk.Label(frame_form, text="3.2.5 Agendar Visita (AAAA-MM-DD HH:MM):").grid(row=8, column=0, sticky="w", pady=2)
        self.entry_fecha = ttk.Entry(frame_form, width=32)
        self.entry_fecha.grid(row=9, column=0, pady=(0, 15), sticky="we")
        self.entry_fecha.insert(0, "2026-09-30 10:00")

        # BOTONES
        btn_guardar = ttk.Button(frame_form, text="Guardar Pedido", command=self._guardar_pedido)
        btn_guardar.grid(row=10, column=0, pady=5, sticky="we")

        btn_eliminar = ttk.Button(frame_form, text="Eliminar Seleccionado", command=self._eliminar_pedido)
        btn_eliminar.grid(row=11, column=0, pady=5, sticky="we")

        # ----------------------------------------------------
        # TABLA DE VISUALIZACIÓN (Treeview)
        # ----------------------------------------------------
        columnas = ("ID", "Cliente", "Dirección", "Inconveniente", "Técnico", "Fecha Visita")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Dirección", text="Dirección")
        self.tabla.heading("Inconveniente", text="Inconveniente")
        self.tabla.heading("Técnico", text="Técnico")
        self.tabla.heading("Fecha Visita", text="Fecha/Hora")

        self.tabla.column("ID", width=35, anchor="center")
        self.tabla.column("Cliente", width=120)
        self.tabla.column("Dirección", width=120)
        self.tabla.column("Inconveniente", width=140)
        self.tabla.column("Técnico", width=100)
        self.tabla.column("Fecha Visita", width=110)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ----------------------------------------------------
    # MÉTODOS DE CONTROL
    # ----------------------------------------------------
    def _guardar_pedido(self):
        cliente = self.entry_cliente.get().strip()
        direccion = self.entry_direccion.get().strip()
        inconveniente = self.text_inconveniente.get("1.0", tk.END).strip()
        tecnico = self.combo_tecnico.get()
        fecha = self.entry_fecha.get().strip()

        if not (cliente and direccion and inconveniente and fecha):
            messagebox.showwarning("Campos Incompletos", "Todos los campos son obligatorios.")
            return

        self.db.guardar_pedido(cliente, direccion, inconveniente, tecnico, fecha)
        messagebox.showinfo("Éxito", "Pedido de servicio técnico guardado correctamente.")
        
        self._limpiar_formulario()
        self._cargar_pedidos()

    def _cargar_pedidos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for registro in self.db.obtener_todos_los_pedidos():
            self.tabla.insert("", "end", values=registro)

    def _eliminar_pedido(self):
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado:
            messagebox.showwarning("Atención", "Seleccione un registro de la tabla para eliminar.")
            return

        confirmacion = messagebox.askyesno("Confirmación", "¿Desea eliminar el pedido seleccionado?")
        if confirmacion:
            pedido_id = self.tabla.item(item_seleccionado[0])['values'][0]
            self.db.eliminar_pedido(pedido_id)
            self._cargar_pedidos()

    def _limpiar_formulario(self):
        self.entry_cliente.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.text_inconveniente.delete("1.0", tk.END)
        self.entry_fecha.delete(0, tk.END)


# ==========================================
# PUNTO DE ENTRADA PRINCIPAL
# ==========================================
if __name__ == "__main__":
    db = BaseDatosService()
    # Iniciar primero con la pantalla de autenticación
    ventana_login = VentanaLogin(db)
    ventana_login.mainloop()