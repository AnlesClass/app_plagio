import pandas as pd
from tkinter import filedialog, messagebox
from functions.operating_functions.LRPD import tabla_resultados

# Función para seleccionar un archivo Excel
def seleccionar_ruta(opc, entrada):
    if opc == 0:
        archivo = filedialog.askopenfilename(
        title="Seleccionar Archivo Excel",
        filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )
        if archivo:
            entrada.delete(0, 'end')
            entrada.insert(0, archivo)
    if opc == 1:
        carpeta = filedialog.askdirectory(title="Seleccionar Carpeta")
        if carpeta:
            entrada.delete(0, 'end')
            entrada.insert(0, carpeta)


## Función para genere Excel con la limpieza de datos de Resultados
def generarExcel(entrada, salida):
    try:
        tabla = tabla_resultados(entrada)
        out_path = f"{salida}/nuevo.xlsx" 

        tabla.to_excel(out_path, index=False)  
        messagebox.showinfo("Éxito", f"Archivo exportado en: {out_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar el archivo: {str(e)}")
