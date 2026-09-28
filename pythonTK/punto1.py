#Está desarrollada bajo el paradigma de Programación Orientada a Objetos (POO) y utiliza el gestor de geometría grid()
#asegurando un manejo correcto de errores de división por cero y entradas matemáticas no válidas
#CALCULADORA

import tkinter as tk
from tkinter import ttk

class Calculadora(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora - Tkinter")
        self.geometry("320x420")
        self.resizable(False, False)

        # Cadena de texto para evaluar la expresión
        self.expresion = ""
        self.pantalla_var = tk.StringVar()

        self._crear_interfaz()

    def _crear_interfaz(self):
        # Pantalla de visualización
        pantalla = ttk.Entry(
            self, 
            textvariable=self.pantalla_var, 
            font=("Consolas", 20), 
            justify="right", 
            state="readonly"
        )
        pantalla.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=15, padx=10, pady=15, sticky="ew")

        # Disposición de botones (Texto, Fila, Columna)
        botones = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3),
        ]

        # Creación dinámica de botones en la cuadrícula
        for (texto, fila, columna) in botones:
            btn = ttk.Button(self, text=texto, command=lambda t=texto: self._al_presionar(t))
            btn.grid(row=fila, column=columna, sticky="nsew", padx=3, pady=3)

        # Configuración de pesos para redimensionamiento uniforme
        for i in range(5):
            self.rowconfigure(i, weight=1)
        for j in range(4):
            self.columnconfigure(j, weight=1)

    def _al_presionar(self, caracter):
        if caracter == 'C':
            self.expresion = ""
        elif caracter == '=':
            try:
                # Evaluación de la expresión matemática
                self.expresion = str(eval(self.expresion))
            except ZeroDivisionError:
                self.expresion = "Error: Div por 0"
            except Exception:
                self.expresion = "Error"
        else:
            # Si venimos de un error, reseteamos la pantalla
            if self.expresion in ["Error", "Error: Div por 0"]:
                self.expresion = ""
            self.expresion += str(caracter)

        self.pantalla_var.set(self.expresion)

if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()