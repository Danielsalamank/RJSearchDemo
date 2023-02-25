import os
from flask import Flask, render_template, request
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Obtener la consulta del usuario
        query = request.form['query']
        
        # Obtener todos los public en la carpeta "public"
        files = [f for f in os.listdir('public') if os.path.isfile(os.path.join('public', f))]
        
        # Realizar la búsqueda y generar los resúmenes de los public relevantes
        results = []
        for file in files:
            if file.endswith('.htm'):
                with open(os.path.join('public', file), 'r') as f:
                    text = f.read()
                summary, title, article_num = generate_summary(text, query, file)
                if summary is not None:
                    results.append((title, summary, file, article_num))
        
        return render_template('search.html', results=results)
    else:
        return render_template('search.html')

def generate_summary(text, query, file):
    # Preprocesamiento del texto y la consulta
    text = text.lower()
    query = query.lower()
    stop_words = set(stopwords.words('spanish'))
    stemmer = SnowballStemmer('spanish')
    sentences = sent_tokenize(text)
    word_frequencies = {}
    for word in query.split():
        word = stemmer.stem(word)
        if word not in stop_words:
            for sentence in sentences:
                if word in sentence.lower():
                    if sentence not in word_frequencies:
                        word_frequencies[sentence] = 1
                    else:
                        word_frequencies[sentence] += 1
    maximum_frequency = max(word_frequencies.values())
    for sentence in word_frequencies.keys():
        word_frequencies[sentence] = (word_frequencies[sentence] / maximum_frequency)
    
    # Generar el resumen
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for query_word in query.split():
            if stemmer.stem(query_word) in sentence.lower():
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies.get(sentence, 0)
                else:
                    sentence_scores[sentence] += word_frequencies.get(sentence, 0)
    if len(sentence_scores) == 0:
        return None, None, None
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary = ' '.join(summary_sentences[:3])
    article_num = 0
    for i, sentence in enumerate(sentences):
        if sentence in summary_sentences:
            article_num = i + 1
            break
    title = os.path.splitext(file)[0]
    return summary, title, article_num

@app.route('/public/<filename>')
def view_file(filename):
    return app.send_static_file(os.path.join('public', filename))

if __name__ == '__main__':
    app.run()
