import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['GET'])
def buscar():
    # Obtiene el término de búsqueda de la solicitud del usuario
    query = request.args.get('q')

    # Busca en la carpeta especificada y devuelve una lista de archivos que contienen el término de búsqueda
    resultados = buscar_archivos(query)

    # Genera un resumen para cada archivo encontrado y muestra los resultados al usuario
    html_resultados = ''
    for resultado in resultados:
        resumen = generar_resumen(resultado)
        html_resultados += '<p><strong>' + resultado + '</strong></p>'
        html_resultados += '<p>' + resumen + '</p>'

    return html_resultados

def buscar_archivos(query):
    archivos = []
    for archivo in os.listdir('/ruta/a/la/carpeta'):
        if archivo.endswith(".txt"):
            archivo_ruta = os.path.join('/ruta/a/la/carpeta', archivo)
            with open(archivo_ruta, "r", encoding="utf-8") as f:
                texto = f.read()
                if query in texto:
                    archivos.append(archivo)
    return archivos

def generar_resumen(archivo):
    with open(os.path.join('/ruta/a/la/carpeta', archivo), "r", encoding="utf-8") as f:
        texto = f.read()
        nlp = spacy.load('es_core_news_sm')
        doc = nlp(texto)
        # Genera el resumen utilizando técnicas de resumen automático
        # (por ejemplo, extracción de frases clave)
        sentences = []
        for sent in doc.sents:
            score = 0
            for token in sent:
                if token.text.lower() not in STOP_WORDS:
                    score += token.vector[0]
            sentences.append((sent, score))
        sentences.sort(key=lambda x: x[1], reverse=True)
        top_sent = sentences[0][0].text
        return top_sent

if __name__ == '__main__':
    app.run()
