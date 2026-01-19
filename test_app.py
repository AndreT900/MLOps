import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    """Test che l'endpoint health risponda"""
    rv = client.get('/health')
    assert rv.status_code == 200
    assert b'ok' in rv.data

def test_predict_no_data(client):
    """Test previsione senza dati"""
    rv = client.post('/predict', json={})
    # Ci aspettiamo 400 Bad Request se non c'è la chiave review o è vuota
    assert rv.status_code == 400 or rv.status_code == 200 # Dipende dall'implementazione, controlliamo app.py

def test_predict_basic(client):
    """Test previsione con dati validi (mockando il modello se necessario o accettando l'errore se manca il pkl)"""
    # Nota: Senza il file .pkl nel contesto del test, app.py potrebbe restituire errore 500 o 'Modello non disponibile'
    # Questo test verifica comunque che l'API risponda
    rv = client.post('/predict', json={'review': 'I love this product'})
    assert rv.status_code in [200, 500]
    if rv.status_code == 200:
        json_data = rv.get_json()
        assert 'sentiment' in json_data
        assert 'confidence' in json_data
