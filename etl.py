import re

def limpiar_reglamento(archivo_entrada, archivo_salida, mantener_articulos=True):
    """
    Limpia el texto de un reglamento interno.
    
    Args:
    - archivo_entrada (str): Ruta del archivo de texto con el reglamento original.
    - archivo_salida (str): Ruta donde se guardará el texto limpio.
    - mantener_articulos (bool): Si True, conserva los números de artículo (e.g., "Art.1.-").
    
    Returns:
    - None
    """
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
            texto = archivo.read()

        # Eliminar encabezados como "CAPÍTULO X" y secciones en mayúsculas
        texto_limpio = re.sub(r'CAP[IÍ]TULO\s+\d+', '', texto, flags=re.IGNORECASE)
        texto_limpio = re.sub(r'\n[A-ZÁÉÍÓÚÑ\s]+(?=\n)', '', texto_limpio, flags=re.IGNORECASE)

        # Limpiar la numeración de artículos si no se desea conservar
        if not mantener_articulos:
            texto_limpio = re.sub(r'Art\.\s?\d+\.-', '', texto_limpio)

        # Eliminar líneas en blanco redundantes
        texto_limpio = re.sub(r'\n\s*\n', '\n', texto_limpio).strip()

        # Guardar el texto limpio
        with open(archivo_salida, 'w', encoding='utf-8') as archivo:
            archivo.write(texto_limpio)

        print(f"Texto limpio guardado en: {archivo_salida}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_entrada}'. Verifica la ruta.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Bloque principal para ejecutar el script
if __name__ == "__main__":
    # Especifica las rutas a los archivos
    archivo_entrada = "dataset/reglamento.txt"  # Cambia esto a la ruta de tu archivo de entrada
    archivo_salida = "dataset/reglamento_limpio.txt"  # Cambia esto si deseas otro nombre de salida

    # Llama a la función con las opciones deseadas
    mantener_articulos = True  # Cambia a False si no quieres conservar los números de artículo
    limpiar_reglamento(archivo_entrada, archivo_salida, mantener_articulos)
