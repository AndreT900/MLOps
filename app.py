import pickle
from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# --- NUOVE METRICHE PERSONALIZZATE ---

# 1. Contatore per la distribuzione delle classi (Drift)
# Labels: 'sentiment' ci permetterà di filtrare per positivo/negativo in Grafana
sentiment_counter = Counter(
    'model_predictions_total', 
    'Totale previsioni per tipo di sentimento', 
    ['sentiment']
)

# 2. Istogramma per la lunghezza del testo (Data Quality)
# Buckets definisce le fasce di lunghezza (es. 0-50 caratteri, 50-100, ecc.)
review_length_histogram = Histogram(
    'review_length_chars', 
    'Lunghezza delle recensioni in caratteri',
    buckets=[50, 100, 200, 500, 1000, float('inf')]
)

# Caricamento Modello
MODEL_FILE = 'sentimentanalysismodel.pkl'
try:
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print(f"Errore caricamento modello: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Modello non disponibile'}), 500

    data = request.get_json()
    review = data.get('review', '')

    if not review:
        return jsonify({'error': 'Testo vuoto'}), 400

    # --- REGISTRAZIONE METRICHE ---
    
    # Registra la lunghezza del testo
    review_length_histogram.observe(len(review))

    try:
        prediction = model.predict([review])
        result = prediction[0] # Es: "positive"
        
        # Registra quale sentimento è stato predetto
        sentiment_counter.labels(sentiment=result).inc()

        return jsonify({
            'sentiment': result,
            'review_length': len(review)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint Opzionale per il Feedback
feedback_counter = Counter(
    'model_feedback_total',
    'Feedback utente sulla correttezza',
    ['correct'] # 'true' o 'false'
)

@app.route('/feedback', methods=['POST'])
def feedback():
    # L'utente invia: {"correct": true} se ci abbiamo azzeccato
    data = request.get_json()
    is_correct = str(data.get('correct', 'false')).lower()
    
    feedback_counter.labels(correct=is_correct).inc()
    return jsonify({'status': 'feedback received'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)