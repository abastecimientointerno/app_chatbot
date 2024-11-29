import os
import json
import google.generativeai as genai
import tiktoken


# Configuración de la API de Gemini
genai.configure(api_key='AIzaSyCRwaF9PSGcVpQ_-a_SGJOX1XkffNs_6uM')

def generar_preguntas_respuestas(texto_reglamento):
    """
    Genera preguntas y respuestas para cada artículo usando la API de Gemini.
    Incluye contexto explícito en el dataset generado.
    """
    # Modelo a utilizar
    model = genai.GenerativeModel('gemini-pro')
    
    # Dividir el reglamento en artículos
    articulos = texto_reglamento.split('Art.')
    
    # Remover entradas vacías y limpiar texto
    articulos = [art.strip() for art in articulos if art.strip()]
    
    dataset = []
    
    # Límite de tokens para evitar exceder el límite de la API
    tokenizer = tiktoken.get_encoding("cl100k_base")
    
    for i, articulo in enumerate(articulos, 1):
        try:
            # Truncar el artículo si es demasiado largo
            tokens = tokenizer.encode(articulo)
            if len(tokens) > 2000:
                articulo = tokenizer.decode(tokens[:2000])
            
            # Crear prompt para la API
            prompt = f"""
Eres un asistente experto en reglamentos laborales. Genera 5 preguntas relevantes con sus respuestas claras basadas en el siguiente artículo del reglamento interno de trabajo (Artículo {i}).

Artículo:
{articulo}

Formato de respuesta:
Pregunta 1: [Pregunta]
Respuesta 1: [Respuesta]
... (hasta 5 preguntas y respuestas)
"""
            respuesta = model.generate_content(prompt)
            
            # Verificar si la respuesta contiene texto
            if not respuesta or not respuesta.text:
                raise ValueError(f"No se generó contenido para el artículo {i}")
            
            # Parsear las preguntas y respuestas
            lineas = [line.strip() for line in respuesta.text.split('\n') if line.strip()]
            for j in range(0, len(lineas), 2):
                if j+1 < len(lineas):
                    pregunta = lineas[j].replace('Pregunta', '').split(':', 1)[-1].strip()
                    respuesta_texto = lineas[j+1].replace('Respuesta', '').split(':', 1)[-1].strip()
                    
                    if pregunta and respuesta_texto:
                        # Agregar entrada al dataset
                        dataset.append({
                            'contexto': articulo,
                            'pregunta': pregunta,
                            'respuesta': respuesta_texto
                        })
        
        except Exception as e:
            print(f"Error procesando artículo {i}: {e}")
    
    return dataset

def guardar_dataset(dataset, nombre_archivo='dataset_reglamento.json'):
    """
    Guarda el dataset generado en un archivo JSON.
    """
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(dataset, archivo, ensure_ascii=False, indent=2)
        print(f"Dataset guardado en {nombre_archivo}")
    except Exception as e:
        print(f"Error al guardar el dataset: {e}")

def main():
    """
    Función principal para ejecutar el script.
    """
    ruta_archivo = 'dataset/reglamento_limpio.txt'
    if not os.path.exists(ruta_archivo):
        print(f"El archivo {ruta_archivo} no existe. Por favor, verifica la ruta.")
        return
    
    # Leer el reglamento desde un archivo
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        texto_reglamento = archivo.read()
    
    print("Generando el dataset...")
    dataset = generar_preguntas_respuestas(texto_reglamento)
    
    if dataset:
        # Guardar el dataset
        guardar_dataset(dataset)
        print(f"Total de ejemplos generados: {len(dataset)}")
    else:
        print("No se generó ningún ejemplo. Revisa el texto del reglamento o la configuración de la API.")

if __name__ == '__main__':
    main()
