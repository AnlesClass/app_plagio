import pandas as pd
from tkinter import filedialog, messagebox
from functions.operating_functions.LRPD import tabla_resultados, generar_regresion_lineal
from pathlib import Path

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
def generarCarpeta(entrada, salida):
    try:
        
        # Creacións de carpetas
        ruta_principal = f"{salida}/LRPD_Estadistica"
        carpeta_principal = Path(ruta_principal)
        carpeta_excels = carpeta_principal / "Excels"
        carpeta_imagenes = carpeta_principal / "Imagenes"
        carpeta_excels.mkdir(parents=True, exist_ok=True)
        carpeta_imagenes.mkdir(parents=True, exist_ok=True)

        # Agregar Excel "ResultadosLimpios" en la carpeta "Excels"
        ruta_resultados_limpios = f"{ruta_principal}/Excels/ResultadosLimpios.xlsx"
        tabla = tabla_resultados(entrada)
        tabla.to_excel(ruta_resultados_limpios, index=False)  
        
        ## Agregar "Graficas de regresion lineal" a la carpeta "Imagenes"
        ruta_regresion_lineal = f"{ruta_principal}/Imagenes/(Resultados)_RegresionLineal.png"
        generar_regresion_lineal(tabla, ruta_regresion_lineal)
        
        
        messagebox.showinfo("Éxito", f"Archivo exportado en: {ruta_resultados_limpios}")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar el archivo: {str(e)}")
