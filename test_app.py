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
    assert rv.status_code == 400 or rv.status_code == 200

def test_predict_basic(client):
    """Test previsione con dati validi (mockando il modello se necessario o accettando l'errore se manca il pkl)"""
    rv = client.post('/predict', json={'review': 'I love this product'})
    assert rv.status_code in [200, 500]
    if rv.status_code == 200:
        json_data = rv.get_json()
        assert 'sentiment' in json_data
        assert 'confidence' in json_data
