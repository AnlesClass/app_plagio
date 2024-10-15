import pandas as pd
import re

# Cargar el archivo Excel para analizar su contenido
file_path = 'Excels\logs-exam.xlsx'
xls = pd.ExcelFile(file_path)

# Mostrar las hojas del archivo
sheet_names = xls.sheet_names
sheet_names

# Cargar la hoja 'Sheet1' para analizar las primeras filas
df = pd.read_excel(file_path, sheet_name='Sheet1')
df = pd.ExcelWriter

# Mostrar las primeras filas del DataFrame para revisar la estructura
df.head()

# Función para extraer el ID de usuario del campo 'Descripción'
def extract_user_id(description):
    match = re.search(r"The user with id '(\d+)'", description)
    if match:
        return int(match.group(1))
    return None

# Crear una nueva columna con el ID extraído
df['User ID'] = df['Descripción'].apply(extract_user_id)

# Mostrar las primeras filas con la nueva columna
df[['Descripción', 'User ID']].head()

# Guardar el archivo actualizado en un nuevo archivo Excel
df.to_excel('nuevo_logs_adp_with_user_ids.xlsx', index=False)