import pandas as pd
from tkinter import filedialog, messagebox
from functions.operating_functions.LRPD import *;
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
def generarCarpeta(primera_entrada,segunda_entrada, salida):
    try:
        # Creacións de carpetas
        ruta_principal = f"{salida}/LRPD_Estadistica"
        carpeta_principal = Path(ruta_principal)
        carpeta_excels = carpeta_principal / "Excels"
        carpeta_imagenes = carpeta_principal / "Imagenes"
        carpeta_excels.mkdir(parents=True, exist_ok=True)
        carpeta_imagenes.mkdir(parents=True, exist_ok=True)

#----------EXCELS---------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Agregar Excel "ResultadosLimpios" en la carpeta "Excels"
        ruta_resultados_limpios = f"{ruta_principal}/Excels/ResultadosLimpios.xlsx"
        tabla_resultados_limpios = tabla_resultados(segunda_entrada)
        tabla_resultados_limpios.to_excel(ruta_resultados_limpios, index=False)        
        
        # Agregar Excel "RegistrosLimpios" en la carpeta "Excels"
        ruta_registros_limpios = f"{ruta_principal}/Excels/RegistrosLimpios.xlsx"
        tabla_registros_limpios = tabla_registro(primera_entrada)
        tabla_registros_limpios.to_excel(ruta_registros_limpios, index=False)
        
#----------IMAGENES---------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Agregar "Graficas de regresion lineal" a la carpeta "Imagenes"
        ruta_regresion_lineal = f"{ruta_principal}/Imagenes/(Resultados)_RegresionLineal.png"
        generar_regresion_lineal(tabla_resultados_limpios, ruta_regresion_lineal)
        
        # Agregar "Graficos de Iforest" a la carpeta "Imagenes"
        ruta_Iforest = f"{ruta_principal}/Imagenes/(Resultados)_Iforest.png"
        generar_iforest(tabla_resultados_limpios, ruta_Iforest)
        ruta_polinomica = f"{ruta_principal}/Imagenes/(Resultados)_polinomica.png"
        generar_polinomico(tabla_resultados_limpios, ruta_polinomica)

        messagebox.showinfo("Éxito", f"Archivo exportado en: {ruta_resultados_limpios}")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar el archivo: {str(e)}")
