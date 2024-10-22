import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
## Función para retornar la tabla Limpia de los Resultados
def tabla_resultados(direccion):
    ## Cambiar la Ruta para el usuario
    df = pd.read_excel(direccion)
    df.head()
    ## LIMPIAR DATOS
    ## Eliminar Columnas innecesarias (Dirección Email, Estado,Iniciado, Finalizado
    df = df.drop(["Dirección Email", "Estado", "Iniciado", "Finalizado"], axis= 1)

    ## Unir nombre y apellido en una columna "Nombre"
    Apellidos = df["Apellido(s)"]
    df = df.drop(["Apellido(s)"], axis=1)
    df["Nombre"] = df["Nombre"] + " " +Apellidos

    ## Cambiar de nombre las columna (Simplicidad en la lecutura)
    df = df.rename(columns={
        'Calificación/20.00': 'Calificación',
        'Q. 1 /2.00': '1',
        'Q. 2 /2.00': '2',
        'Q. 3 /2.00': '3',
        'Q. 4 /2.00': '4',
        'Q. 5 /2.00': '5',
        'Q. 6 /2.00': '6',
        'Q. 7 /2.00': '7',
        'Q. 8 /2.00': '8',
        'Q. 9 /2.00': '9',
        'Q. 10 /2.00': '10',
    })

    ## Eliminar ultima fila (Promedio)
    df = df.drop(df.index[-1])

    ## Funcion para convertir el texto " x mins y segundos" de la columna Duración a un valor entero de segundos
    def convertir_segundos(texto):
        datos = texto.split() ## Dividir la cadena de texto por espacios
        minutos = int(datos[0])
        segundo = int(datos[2])
        return minutos*60 + segundo

    ## Utilizar el metodo apply (tiene como parametro una función) para cambiar el formato a valor entero en la columna "Duración"
    df["Duración"] = df["Duración"].apply(convertir_segundos)

    ## Convertir todas las columnas de tipo float a enteros
    df = df.apply(lambda x: x.astype(int) if x.dtype == "float64" else x)

    ## Mostrar DataFrame Limpio
    return df
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## GRAFICAS PRUEBA
def generar_regresion_lineal(data_frame, ruta_imagen):
    df = data_frame
    ## conseguir los valores de la funcion linea  y  = ax + b  (en este caso obtenemos a y b)
    a, b = np.polyfit(df['Duración'], df['Calificación'], 1)

    # Forma de la funcion y = ax + b
    y_pred = a * df['Duración'] + b

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Duración'], df['Calificación'], color='blue', label='Datos originales')
    plt.plot(df['Duración'], y_pred, color='red', label='Línea de regresión', linewidth=2)
    plt.title('Regresión Lineal: Calificación - Duración')
    plt.xlabel('Duración (segundos)')
    plt.ylabel('Calificación')
    plt.legend()
    plt.savefig(ruta_imagen, format='png')
