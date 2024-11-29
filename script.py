import csv

# Archivo fuente (el reglamento)
source_file = "fine_tuning/reglamento.txt"
output_file = "fine_tuning/reglamento_preguntas_con_contexto_chatbot_final.csv"

# Leer el reglamento
with open(source_file, "r", encoding="utf-8") as file:
    content = file.read()

# Lista ampliada de preguntas frecuentes y sus palabras clave
faq = [
    {"question": "¿Cuáles son los derechos de los trabajadores?", "keywords": ["derechos", "trabajadores"]},
    {"question": "¿Qué sucede si un trabajador llega tarde?", "keywords": ["llegar tarde", "tardanza"]},
    {"question": "¿Qué hacer si no puedo asistir al trabajo?", "keywords": ["inasistencia", "ausencia"]},
    {"question": "¿Cómo solicito un permiso o licencia?", "keywords": ["permiso", "licencia"]},
    {"question": "¿Qué pasa si incumplo alguna norma del reglamento?", "keywords": ["incumplimiento", "sanción"]},
    {"question": "¿Qué pasa si se me olvida marcar la tarjeta de asistencia?", "keywords": ["olvidar", "marcar", "asistencia"]},
    {"question": "¿Qué beneficios tengo al trabajar durante un feriado?", "keywords": ["feriado", "beneficios"]},
    {"question": "¿Cómo se gestiona el descanso vacacional?", "keywords": ["vacacional", "descanso"]},
    {"question": "¿Puedo cambiar mi turno de trabajo?", "keywords": ["cambiar", "turno", "trabajo"]},
    {"question": "¿Qué pasa si me enfermo y no puedo asistir al trabajo?", "keywords": ["enfermedad", "no asistir", "trabajo"]},
    {"question": "¿Cómo se maneja la confidencialidad de la información?", "keywords": ["confidencialidad", "información"]},
    {"question": "¿Qué pasa si no cumplo con las medidas de seguridad en el trabajo?", "keywords": ["seguridad", "trabajo", "incumplir"]},
    {"question": "¿Qué debo hacer si tengo una queja o reclamación?", "keywords": ["queja", "reclamación"]},
    {"question": "¿Cuáles son las consecuencias de realizar sobretiempo sin autorización?", "keywords": ["sobretimpo", "sin autorización"]},
    {"question": "¿Cómo se lleva a cabo la reubicación dentro de la empresa?", "keywords": ["reubicación", "empresa"]},
    {"question": "¿Qué ocurre si no cumplo con los exámenes médicos ocupacionales?", "keywords": ["exámenes médicos", "ocupacionales", "incumplir"]},
    {"question": "¿Qué hago si quiero tomar un descanso durante la jornada laboral?", "keywords": ["descanso", "jornada laboral"]},
    {"question": "¿Cómo se manejan los permisos por enfermedad?", "keywords": ["permiso", "enfermedad"]},
    {"question": "¿Qué pasa si tengo un conflicto con un compañero de trabajo?", "keywords": ["conflicto", "compañero de trabajo"]},
    {"question": "¿Qué medidas toma la empresa contra el hostigamiento sexual?", "keywords": ["hostigamiento sexual", "medidas"]},
    {"question": "¿Qué hacer si quiero denunciar un acto de discriminación?", "keywords": ["denunciar", "discriminación"]},
    {"question": "¿Cómo se protege la información confidencial en la empresa?", "keywords": ["protección", "información confidencial"]},
    {"question": "¿Qué debo hacer si pierdo un documento importante de trabajo?", "keywords": ["perder", "documento importante"]},
    {"question": "¿Qué pasa si no cumplo con la política de seguridad y salud en el trabajo?", "keywords": ["seguridad", "salud", "incumplir"]},
    {"question": "¿Puedo usar mi celular personal durante el trabajo?", "keywords": ["celular", "trabajo", "personal"]},
    {"question": "¿Cómo puedo saber mis derechos sobre el VIH en la empresa?", "keywords": ["derechos", "VIH", "empresa"]},
    {"question": "¿Qué hacer si me siento discriminado en el trabajo?", "keywords": ["discriminado", "trabajo"]},
    {"question": "¿Cómo solicito el uso del lactario si soy madre trabajadora?", "keywords": ["lactario", "madre trabajadora"]},
    {"question": "¿Puedo cambiar de puesto dentro de la empresa?", "keywords": ["cambiar", "puesto", "empresa"]},
    {"question": "¿Cuáles son las medidas contra la tuberculosis en el lugar de trabajo?", "keywords": ["tuberculosis", "trabajo", "medidas"]},
]

# Procesar el reglamento por capítulos y artículos
data = []

# Dividir el contenido en párrafos para buscar coincidencias
paragraphs = content.split("\n")
for faq_item in faq:
    question = faq_item["question"]
    keywords = faq_item["keywords"]
    
    # Buscar el párrafo que contiene las palabras clave
    relevant_paragraph = ""
    for paragraph in paragraphs:
        if any(keyword in paragraph.lower() for keyword in keywords):
            relevant_paragraph = paragraph.strip()
            break  # Tomamos el primer párrafo relevante
    
    # Crear una respuesta concisa
    answer = ""
    if relevant_paragraph:
        # Resumimos la respuesta sin repetir todo el contexto
        if "derechos" in question.lower():
            answer = "El reglamento establece que los trabajadores tienen derechos que buscan garantizar su bienestar y eficiencia en la empresa."
        elif "tarde" in question.lower():
            answer = "El reglamento establece sanciones para los trabajadores que lleguen tarde de forma reiterada."
        else:
            answer = "Este reglamento regula diversas situaciones laborales como permisos, sanciones y otros derechos de los trabajadores."
    
    # Crear un dataset con el formato de contexto, pregunta y respuesta
    data.append({"context": relevant_paragraph, "question": question, "answer": answer})

# Escribir en un archivo CSV
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["context", "question", "answer"])
    writer.writeheader()
    writer.writerows(data)

print(f"Dataset con preguntas generales y contexto natural generado en: {output_file}")
