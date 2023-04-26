import pdfplumber
import tabula
import pandas as pd

def is_empty_dataframe(df):
    return df.empty or all(df.dropna(axis=1, how='all').dropna(axis=0, how='all').columns.isnull())

def extraer_tablas_pdf(archivo_pdf: str) -> list:
    """ 
    `archivo_pdf`: una cadena que contiene el nombre del archivo PDF que se va a procesar.
    `tablas`: una lista de DataFrames que contienen las tablas extraídas del PDF.
    Esta función utiliza la biblioteca tabula para extraer todas las tablas de un archivo PDF y devuelve una lista de DataFrames que representan las tablas extraídas.
    """
    tablas = []
    with pdfplumber.open(archivo_pdf) as pdf:
        for page in pdf.pages:
            # Primero intenta extraer la tabla sin estrategia
            tabla = page.extract_table()
            
            if tabla:
                df = pd.DataFrame(tabla[1:], columns=tabla[0])
                print('Aqui esta el df ' + str(df))
                if is_empty_dataframe(df):
                    tablas = tabula.read_pdf(archivo_pdf, pages='all', multiple_tables=True, encoding='latin1', stream=True, guess=False)
                    print("Aqui entro vacio")
                    print(tablas)
                    return tablas
                else:
                    print("Aqui entro lleno")
                    tablas = tabula.read_pdf(archivo_pdf, pages='all', multiple_tables=True, encoding='latin1')
    print(tablas)
    return tablas

def procesar_tablas(tablas: list) -> list:
    """ 
    `tablas`: una lista de DataFrames que contienen las tablas extraídas del PDF.
    `datos_procesados`: una lista de DataFrames que contienen las tablas procesadas.
    Esta función procesa las tablas extraídas eliminando filas y columnas vacías.   
    """
    datos_procesados = []
    for tabla in tablas:
        tabla_limpia = tabla.dropna(axis=1, how='all').dropna(axis=0, how='all')
        datos_procesados.append(tabla_limpia)
    return datos_procesados

def guardar_en_excel(datos, nombre_archivo_salida):
    """ 
    `datos`: una lista de DataFrames que contienen las tablas procesadas.
    `nombre_archivo_salida`: una cadena que contiene el nombre del archivo de Excel de salida.
    `None`: esta función no devuelve ningún valor.
    Esta función utiliza la biblioteca pandas para guardar los datos procesados en un archivo de Excel. 
    Crea un objeto ExcelWriter y escribe cada DataFrame en una hoja de cálculo separada en el archivo de Excel de salida. Finalmente, guarda el archivo de Excel.
    """
    with pd.ExcelWriter(nombre_archivo_salida, engine='openpyxl') as writer:
        for i, tabla in enumerate(datos):
            tabla.to_excel(writer, index=False, sheet_name=f'Hoja{i+1}')
        writer.book.save(nombre_archivo_salida)
