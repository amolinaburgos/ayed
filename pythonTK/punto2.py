#La solución implementa la persistencia en base de datos (repair_center.db), el formulario con los campos solicitados y una vista de tabla
# interactiva (ttk.Treeview) para consultar y gestionar los registros agendados en tiempo real.


import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# 1. GESTIÓN DE LA BASE DE DATOS (SQLite)
# ==========================================
class BaseDatosService:
    def __init__(self, db_name="repair_center.db"):
        self.db_name = db_name
        self._crear_tabla()

    def _obtener_conexion(self):
        return sqlite3.connect(self.db_name)

    def _crear_tabla(self):
        """Crea la tabla pedidos si no existe"""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
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
            conn.commit()

    def guardar_pedido(self, cliente, direccion, inconveniente, tecnico, fecha_visita):
        """Inserta un nuevo pedido en la base de datos (Puntos 3.2.1 a 3.2.5)"""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pedidos (cliente, direccion, inconveniente, tecnico, fecha_visita)
                VALUES (?, ?, ?, ?, ?)
            """, (cliente, direccion, inconveniente, tecnico, fecha_visita))
            conn.commit()

    def obtener_todos_los_pedidos(self):
        """Consulta todos los registros agendados"""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
            return cursor.fetchall()

    def eliminar_pedido(self, pedido_id):
        """Elimina un registro seleccionado por su ID"""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
            conn.commit()


# ==========================================
# 2. INTERFAZ GRÁFICA (Tkinter POO)
# ==========================================
class AppRepairCenter(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("Repair Center - Administración de Pedidos")
        self.geometry("900x550")
        self.resizable(True, True)

        self._crear_interfaz()
        self._cargar_pedidos()

    def _crear_interfaz(self):
        # Panel Izquierdo: Formulario de Ingreso de Datos
        frame_form = ttk.LabelFrame(self, text=" Agendar Pedido de Servicio Técnico ", padding="15")
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        # Panel Derecho: Visualización y eliminación de pedidos
        frame_tabla = ttk.LabelFrame(self, text=" Historial de Pedidos Agendados ", padding="10")
        frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # ----------------------------------------------------
        # CAMPOS DEL FORMULARIO
        # ----------------------------------------------------
        # 3.2.1 Apellido y Nombre
        ttk.Label(frame_form, text="3.2.1 Apellido y Nombre del Cliente:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_cliente = ttk.Entry(frame_form, width=32)
        self.entry_cliente.grid(row=1, column=0, pady=(0, 8), sticky="we")

        # 3.2.2 Dirección (Calle y Altura)
        ttk.Label(frame_form, text="3.2.2 Dirección (Calle y Altura):").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_direccion = ttk.Entry(frame_form, width=32)
        self.entry_direccion.grid(row=3, column=0, pady=(0, 8), sticky="we")

        # 3.2.3 Inconveniente
        ttk.Label(frame_form, text="3.2.3 Inconveniente informado:").grid(row=4, column=0, sticky="w", pady=2)
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
        self.entry_fecha.insert(0, "2026-03-30 10:00")

        # BOTONES DE ACCIÓN
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

        # Validación de campos
        if not (cliente and direccion and inconveniente and fecha):
            messagebox.showwarning("Atención", "Todos los campos del formulario son obligatorios.")
            return

        # Persistir en base de datos SQLite
        self.db.guardar_pedido(cliente, direccion, inconveniente, tecnico, fecha)
        messagebox.showinfo("Éxito", "El pedido de servicio técnico fue agendado correctamente.")
        
        self._limpiar_formulario()
        self._cargar_pedidos()

    def _cargar_pedidos(self):
        """Refresca las filas del Treeview desde SQLite"""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for registro in self.db.obtener_todos_los_pedidos():
            self.tabla.insert("", "end", values=registro)

    def _eliminar_pedido(self):
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado:
            messagebox.showwarning("Atención", "Seleccione un pedido de la lista para eliminar.")
            return

        confirmacion = messagebox.askyesno("Confirmar", "¿Desea eliminar el pedido seleccionado?")
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
    app = AppRepairCenter(db)
    app.mainloop()