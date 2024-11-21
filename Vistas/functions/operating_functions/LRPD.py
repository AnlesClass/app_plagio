import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import random

#---LIMPIAR TABLA RESULTADOS----------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

#---GRAFICOS DE RESULTADOS----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Grafico polinomica
def generar_polinomico(data_frame, ruta_imagen):
    sns.lmplot(
    data=data_frame,
    x="Duración",
    y="Calificación",
    order=5,  # Ajuste polinómico de segundo grado
    ci=None,  # Elimina el intervalo de confianza
    )
    plt.savefig(ruta_imagen, format="png")

## Grafico Regresion Lineal 
def generar_regresion_lineal(data_frame, ruta_imagen):
    df = data_frame
    a, b = np.polyfit(df['Duración'], df['Calificación'], 1)
    promedio_duracion =  df["Duración"].mean()
    desviacion_duracion = df["Duración"].std()
    promedio_calificacion =  df["Calificación"].mean()
    desviacion_calificacion = df["Calificación"].std()
    separacion= "____________________________________________"
    informacion = f"""Coeficiente de correlación: {a:.4f}\n{separacion}
        \nPromedio de Duración: {promedio_duracion:.2f}
        \nDesviación estándar de Duración: {desviacion_duracion:.2f}\n{separacion}
        \nPromedio de Calificación {promedio_calificacion:.2f}
        \nDesviación estándar de Calificación: {desviacion_calificacion:.2f}"""    

    sns.lmplot(
        data=df,
        x="Duración",
        y="Calificación",
        scatter_kws={'s': 50, 'alpha': 0.7},  
        line_kws={'color': 'coral', 'linewidth': 2},  
        height=8,
        aspect=1.5  
    )
    plt.title("Regresion Lineal (Duración, Calificación)")

    plt.text(
        1, 0.5, informacion, 
        transform=plt.gca().transAxes, 
        fontsize=12, 
        verticalalignment='center', 
        horizontalalignment='left', 
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray', boxstyle='round,pad=0.5')
    )
    plt.tight_layout()    
    plt.savefig(ruta_imagen, format='png')

## Grafico de Iforest
def generar_iforest(data_frame,data_action_result, ruta_imagen):
    df = data_frame
    df_acciones = data_action_result
    df_ids_unicos = df_acciones[['Id', 'Usuario']].drop_duplicates()
    
    df_total = df_ids_unicos[df_ids_unicos['Usuario'].isin(df['Nombre'])] 
    df_total = df_total.merge(df[['Nombre', 'Duración', 'Calificación']], 
                              left_on='Usuario', 
                              right_on='Nombre', 
                              how='inner')
    
    df_total.drop(columns=['Nombre'], inplace=True)
    
    # Normalizar las características 'Duración' y 'Calificación' en df_total
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_total[['Duración', 'Calificación']])
    
    contaminaciones = [0.01, 0.05, 0.1]
    
    fig, axes = plt.subplots(1, 3, figsize=(25, 10), sharex=True, sharey=True)
    
    for i, cont in enumerate(contaminaciones):
        model = IsolationForest(contamination=cont, random_state=42)
        model.fit(df_scaled)
        
        df_total[f'Anomalia_{cont}'] = model.predict(df_scaled)
        
        sns.scatterplot(
            data=df_total, 
            x='Duración', 
            y='Calificación', 
            hue=f'Anomalia_{cont}', 
            sizes=(20, 200), 
            ax=axes[i], 
            palette='coolwarm',
            marker="x",
            s=140
        )
    
        axes[i].set_title(f'Contaminación: {cont}')
        axes[i].set_xlabel('Duración')
        axes[i].set_ylabel('Calificación')
    
        anomalias = df_total[df_total[f'Anomalia_{cont}'] == -1]
    
        table_data = anomalias[['Id', 'Duración', 'Calificación']] 
    
        # Añadir la tabla debajo de cada gráfico
        axes[i].table(cellText=table_data.values, 
                      colLabels=table_data.columns, 
                      loc='bottom', 
                      cellLoc='center', 
                      bbox=[0, -0.4, 1, 0.3])
    
    plt.tight_layout()
    plt.savefig(ruta_imagen, format= "png")

# Grafico polinomica
def generar_polinomico(data_frame, ruta_imagen):
    sns.lmplot(
    data=data_frame,
    x="Duración",
    y="Calificación",
    order=5, 
    ci=None, 
    )
    plt.savefig(ruta_imagen, format="png")
    
#-------LIMPIAR TABLA REGISTRO-----------------------------------------------------------------------------------------------------------------------------------------------------------------

## Función para retornar la tabla Limpia de los Registro
def tabla_registro(direccion):
    df = pd.read_excel(direccion)
    eventos_permitidos = ['Intento de examen iniciado', 'Intento de examen enviado', 'Intento de examen actualizado']
    df = df[df['Nombre del evento'].isin(eventos_permitidos)]

    df['Hora'] = df['Hora'].apply(lambda texto: int(texto.split()[1][3:5]) * 60 + int(texto.split()[1][6:8]))

    # Editar la descripción para preguntas específicas
    def editar_descripcion(texto):
        index_start = 52 if "'" in texto[18:20] else 53
        return texto[index_start:index_start + 2].strip("'") if texto[index_start:index_start + 2] == '10' else texto[index_start:index_start + 1]

    df['Descripción'] = df.apply(
        lambda x: editar_descripcion(x['Descripción']) if x['Nombre del evento'] == 'Intento de examen actualizado' else x['Descripción'], 
        axis=1
    )

    # Cambiar descripciones según evento
    df.loc[df['Nombre del evento'] == 'Intento de examen enviado', 'Descripción'] = 'Final'
    df.loc[df['Nombre del evento'] == 'Intento de examen iniciado', 'Descripción'] = 'Inicio'

    # Calcular tiempos y ajustar valores
    df['Tiempo'] = df['Hora'].shift(1) - df['Hora']
    df.loc[df['Descripción'] == '1', 'Tiempo'] = df['Hora'].shift(1) - df['Hora'].shift(-1)
    df.loc[df['Descripción'].isin(['Final', 'Inicio']), 'Tiempo'] = 0
    df['Tiempo'] = df['Tiempo'].apply(lambda x: random.randint(16, 19) if x < 0 else int(x))

    # Eliminar filas no deseadas
    df = df[~df['Descripción'].isin(['Final', 'Inicio'])]

    # Renombrar columna
    df = df.rename(columns={'Nombre completo del usuario': 'Usuario', 'Descripción': 'Pregunta'})

    # Asignar IDs únicos a cada usuario
    df['Id'] = df['Usuario'].map({usuario: idx for idx, usuario in enumerate(df['Usuario'].unique(), start=1)})

    # Reorganizar columnas
    df = df.drop([1615, 1613, 1617, 1600, 1598, 1596]) 
    df = df[['Id', 'Usuario', 'Pregunta', 'Tiempo']]  


    return df


#-------GRAFICOS DE REGISTRO-----------------------------------------------------------------------------------------------------------------------------------------------------------------

#Grafico de Mapa de Calor
def generar_mapa_calor(data_frame, ruta_imagen):
    df = data_frame

    # Calcular el tiempo promedio por cada combinación de usuario y pregunta
    pivot_table = df.pivot_table(values="Tiempo", index="Id", columns="Pregunta", aggfunc="mean")

    # Graficar el heatmap
    plt.figure(figsize=(15, 15))
    sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".1f", cbar_kws={'label': 'Tiempo (segundos)'})
    plt.title("Mapa de Calor del Tiempo Promedio por Usuario y Pregunta")
    plt.xlabel("Pregunta")
    plt.ylabel("Usuario")    
    plt.savefig(ruta_imagen, format="png")

# Grafico de Tabla de Tiempo
def generar_tabla_tiempo(data_frame, ruta_imagen):
    df = data_frame
    # Asegurarse de que la columna 'Preguntas' esté en formato numérico
    df['Pregunta'] = pd.to_numeric(df['Pregunta'], errors='coerce')

    # Crear la tabla dinámica
    pivot_table_sum = df.pivot_table(values="Tiempo", index="Id", columns="Pregunta", aggfunc="sum")

    # Ordenar las columnas de las preguntas numéricamente
    pivot_table_sum = pivot_table_sum[sorted(pivot_table_sum.columns)]

    # Graficar el gráfico de barras apiladas
    pivot_table_sum.plot(kind="bar", stacked=True, figsize=(14, 8), colormap="tab20")
    plt.title("Tiempo Total por Usuario y Pregunta (Barras Apiladas)")
    plt.xlabel("Usuario")
    plt.ylabel("Tiempo (segundos)")
    plt.legend(title="Pregunta", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(ruta_imagen, format="png")



        
        
    

