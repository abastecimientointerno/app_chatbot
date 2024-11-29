import os
import json
import google.generativeai as genai
import tiktoken

# Configuración de la API de Gemini
genai.configure(api_key='AIzaSyCRwaF9PSGcVpQ_-a_SGJOX1XkffNs_6uM')

def generar_preguntas_respuestas(texto_reglamento):
    """
    Genera preguntas y respuestas para cada artículo usando la API de Gemini
    """
    # Modelo a utilizar
    model = genai.GenerativeModel('gemini-pro')
    
    # Dividir el reglamento en artículos
    articulos = texto_reglamento.split('Art.')
    
    # Remover el primer elemento vacío si existe
    articulos = [art for art in articulos if art.strip()]
    
    dataset = []
    
    # Límite de tokens para evitar exceder el límite de la API
    tokenizer = tiktoken.get_encoding("cl100k_base")
    
    for i, articulo in enumerate(articulos, 1):
        try:
            # Truncar el artículo si es demasiado largo
            tokens = tokenizer.encode(articulo)
            if len(tokens) > 2000:
                articulo = tokenizer.decode(tokens[:2000])
            
            # Solicitar generación de preguntas
            prompt = f"""Eres un asistente experto en generar preguntas y respuestas para reglamentos internos de trabajo. 
            Genera 5 preguntas diferentes con sus respectivas respuestas para el siguiente artículo del reglamento interno de trabajo (Artículo {i}):

            {articulo}

            Formato de respuesta:
            Pregunta 1: [Pregunta]
            Respuesta 1: [Respuesta]
            Pregunta 2: [Pregunta]
            Respuesta 2: [Respuesta]
            ... (continúa hasta 5 preguntas)"""
            
            respuesta = model.generate_content(prompt)
            
            # Parsear las preguntas y respuestas
            lineas = respuesta.text.split('\n')
            for j in range(0, len(lineas), 2):
                if j+1 < len(lineas):
                    pregunta = lineas[j].replace('Pregunta:', '').replace('Pregunta 1:', '').replace('Pregunta 2:', '').replace('Pregunta 3:', '').replace('Pregunta 4:', '').replace('Pregunta 5:', '').strip()
                    respuesta_texto = lineas[j+1].replace('Respuesta:', '').replace('Respuesta 1:', '').replace('Respuesta 2:', '').replace('Respuesta 3:', '').replace('Respuesta 4:', '').replace('Respuesta 5:', '').strip()
                    
                    # Agregar al dataset
                    dataset.append({
                        'articulo': i,
                        'pregunta': pregunta,
                        'respuesta': respuesta_texto,
                        'contexto': articulo
                    })
        
        except Exception as e:
            print(f"Error procesando artículo {i}: {e}")
    
    return dataset

def guardar_dataset(dataset, nombre_archivo='dataset_reglamento.json'):
    """
    Guarda el dataset generado en un archivo JSON
    """
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(dataset, archivo, ensure_ascii=False, indent=2)
    print(f"Dataset guardado en {nombre_archivo}")

def main():
    # Leer el reglamento desde un archivo
    with open('dataset/reglamento_limpio.txt', 'r', encoding='utf-8') as archivo:
        texto_reglamento = archivo.read()
    
    # Generar el dataset
    dataset = generar_preguntas_respuestas(texto_reglamento)
    
    # Guardar el dataset
    guardar_dataset(dataset)
    
    # Mostrar estadísticas
    print(f"Total de ejemplos generados: {len(dataset)}")

if __name__ == '__main__':
    main()