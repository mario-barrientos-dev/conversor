import tabula
import pandas as pd

def extraer_tablas_pdf(archivo_pdf):
    tablas = tabula.read_pdf(archivo_pdf, pages='all', multiple_tables=True, encoding='latin1')
    return tablas

def procesar_tablas(tablas):
    datos_procesados = []
    for tabla in tablas:
        tabla_limpia = tabla.dropna(axis=1, how='all').dropna(axis=0, how='all')
        datos_procesados.append(tabla_limpia)
    return datos_procesados

def guardar_en_excel(datos, nombre_archivo_salida):
    with pd.ExcelWriter(nombre_archivo_salida, engine='openpyxl') as writer:
        for i, tabla in enumerate(datos):
            tabla.to_excel(writer, index=False, sheet_name=f'Hoja{i+1}')
        writer.book.save(nombre_archivo_salida)
