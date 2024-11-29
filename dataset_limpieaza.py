import os
import json
import re

def limpiar_texto(texto):
    """
    Función que limpia el texto eliminando caracteres innecesarios y
    mejorando la estructura para hacerla más clara para el modelo.
    """
    # Eliminar asteriscos innecesarios de las preguntas
    texto = re.sub(r'\*\*', '', texto)
    
    # Limpiar espacios adicionales al inicio y fin de la cadena
    texto = texto.strip()
    
    return texto

def procesar_dataset(dataset):
    """
    Procesa el dataset para limpiar y organizar las preguntas y respuestas.
    """
    dataset_limpio = []

    for entrada in dataset:
        # Limpiar el contexto, pregunta y respuesta
        contexto = limpiar_texto(entrada.get('contexto', ''))
        pregunta = limpiar_texto(entrada.get('pregunta', ''))
        respuesta = limpiar_texto(entrada.get('respuesta', ''))

        # Verificar que haya contenido válido en la pregunta y respuesta
        if pregunta and respuesta:
            # Agregar la entrada procesada al dataset limpio
            dataset_limpio.append({
                'contexto': contexto,
                'pregunta': pregunta,
                'respuesta': respuesta
            })
        else:
            print(f"Se omitió una entrada debido a falta de pregunta o respuesta: {entrada}")

    return dataset_limpio

def guardar_dataset_limpio(dataset, nombre_archivo='dataset_reglamento_limpio.json'):
    """
    Guarda el dataset limpio en un archivo JSON.
    """
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(dataset, archivo, ensure_ascii=False, indent=2)
        print(f"Dataset limpio guardado en {nombre_archivo}")
    except Exception as e:
        print(f"Error al guardar el dataset limpio: {e}")

def main():
    """
    Función principal para leer, limpiar y guardar el dataset.
    """
    ruta_archivo = 'dataset_reglamento.json'
    if not os.path.exists(ruta_archivo):
        print(f"El archivo {ruta_archivo} no existe. Por favor, verifica la ruta.")
        return
    
    # Leer el dataset desde un archivo JSON
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        dataset = json.load(archivo)
    
    print("Procesando y limpiando el dataset...")
    dataset_limpio = procesar_dataset(dataset)
    
    if dataset_limpio:
        # Guardar el dataset limpio
        guardar_dataset_limpio(dataset_limpio)
        print(f"Total de ejemplos después de limpieza: {len(dataset_limpio)}")
    else:
        print("El dataset limpio está vacío. Revisa el contenido.")

if __name__ == '__main__':
    main()
