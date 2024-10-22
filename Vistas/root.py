import tkinter as tk # tkinter sirve para crear interfaces gráficas sencillas en Python.
import pandas as pd
from functions.button_functions.funciones import *

# Configuración principal de la ventana
root = tk.Tk() # Instancia. Crea una instancia de ventana
root.title("Sistema de Detección de Datos Anómalos - Plagium 1.0") # Atributo. Muestra un título para la ventana.
root.geometry("410x350")  # Atributo. Tamaño de la ventana
root.resizable(False, False) # Atributo. Deshabilitar escalado en X y Y.
root.configure(bg="#e6daba") # Método. Sirve para configurar diversos atributos del tk.Tk()

# Elementos Visuales - INICIALIZAR
opciones_menu = ["Archivo Excel", "Imágenes PNG"]
opciones = tk.StringVar(root)
opciones.set(opciones_menu[0])

# Elementos Visuales - CREAR
label_curso = tk.Label(root, text="Estadística y\nProbabilidades")

label_registro = tk.Label(root, text="Registros del Examen")
entry_registro = tk.Entry(root, border=2)
button_registro = tk.Button(root, text="Examinar", command= lambda: seleccionar_ruta(0,entry_registro))
label_resultado = tk.Label(root, text="Resultados del Examen")
entry_resultado = tk.Entry(root, border=2)
button_resultado = tk.Button(root, text="Examinar", command= lambda: seleccionar_ruta(0,entry_resultado))
label_tipo_salida = tk.Label(root, text="Tipo de Salida")
combox_tipo_salida = tk.OptionMenu(root, opciones, *opciones_menu)
label_ruta_salida = tk.Label(root, text="Ruta de Salida")
entry_ruta_salida = tk.Entry(root, border=2)
button_ruta_salida = tk.Button(root, text="Examinar", command= lambda: seleccionar_ruta(1,entry_ruta_salida))
button_generar = tk.Button(root, text="Generar Gráficos", command= lambda: generarCarpeta(entry_resultado.get(), entry_ruta_salida.get()))

# Elementos Visuales - CONFIGURAR
label_curso.configure(bg="#e6daba", foreground="#1f1d18", font=("Garamond", 20, "bold"))

label_registro.configure(bg="#e6daba", font=("Arial", 10, "italic"))
label_resultado.configure(bg="#e6daba", font=("Arial", 10, "italic"))
label_tipo_salida.configure(bg="#e6daba", font=("Arial", 10, "italic"))
label_ruta_salida.configure(bg="#e6daba", font=("Arial", 10, "italic"))

entry_registro.insert(0, "Buscar Registro *.xlsx")
combox_tipo_salida.configure(bg="#d5e8d4", borderwidth=0)

# Elementos Visuales - POSICIONAR
label_curso.place(x=200, y=175)

label_registro.place(x=20, y=20)
label_resultado.place(x=20, y=95)
label_tipo_salida.place(x=20, y=160)
label_ruta_salida.place(x=20, y=235)

entry_registro.place(x=20, y=45, width=300) # Distancia Y = 25, para separación 1.5 usaremos 40.
entry_resultado.place(x=20, y=120, width=300)
combox_tipo_salida.place(x=20, y=185, width=150)
entry_ruta_salida.place(x=20, y=260, width=300)

button_registro.place(x=330, y=40) # -5 en y con respecto al elemento a  su lado.
button_resultado.place(x=330, y=115)
button_ruta_salida.place(x=330, y=255)
button_generar.place(x=20, y=300, width=370)

root.mainloop() # Método. Muestra la ventana.

# INFORMACIÓN SOBRE EL USO DE TKINTER
# https://docs.python.org/es/3/library/tkinter.html