# Sentiment Analysis API & Monitoring System

Progetto DevOps per il deploy, monitoraggio e automazione di un modello di Sentiment Analysis.
L'infrastruttura espone una REST API (Flask) per analizzare recensioni e fornisce una pipeline CI/CD COMPLETA con sistema di monitoraggio integrato.

## Stack Tecnologico

*   **App & ML**:Flask, Scikit-learn (modello Pickle pre-addestrato).
*   **Containerizzazione**: Docker & Docker Compose.
*   **CI/CD**: Jenkins (configurazione Docker-in-Docker).
*   **Monitoraggio**: Prometheus (raccolta metriche) + Grafana (dashboard).

## Quick Start 🚀

1.  **Clona il repository**:
    ```bash
    git clone https://github.com/AndreT900/MLOps.git
    cd MLOps
    ```

2.  **Avvia l'ambiente**:
    Lancia tutti i servizi (App, Jenkins, Prometheus, Grafana) con un solo comando:
    ```bash
    docker-compose up -d
    ```

3.  **Verifica lo stato**:
    Controlla che i container siano attivi:
    ```bash
    docker ps
    ```

## Endpoints e Servizi

| Servizio | URL Locale | Credenziali Default | Note |
|---|---|---|---|
| **API Model** | `http://localhost:5000` Endpoint `/predict` |
| **Jenkins** | `http://localhost:8080` | Per la pipeline CI/CD |
| **Grafana** | `http://localhost:3000` | `admin` / `admin`
| **Prometheus** | `http://localhost:9090` | Esplorazione metriche raw |

## Utilizzo API

L'API accetta richieste POST con un JSON contenente il testo della recensione.

**Esempio di richiesta (Terminale):**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"review": "This product is absolutely amazing! I love it."}' \
     http://localhost:5000/predict
```

**Risposta attesa:**
```json
{
  "confidence": 0.95,
  "sentiment": "positive"
}
```

## Struttura Pipeline (Jenkins)

Il `Jenkinsfile` definisce i seguenti stage automatizzati:
1.  **Build**: Crea l'immagine Docker dell'applicazione.
2.  **Unit Tests**: Esegue `pytest` in un container isolato.
3.  **Integration Test**: Lancia un container temporaneo e verifica l'endpoint `/metrics`.
4.  **Deploy**: Aggiorna il container di produzione (`production-model`) senza downtime manuale.

*Nota: La pipeline è configurata per controllare modifiche su GitHub ogni 2 minuti.*


## Sviluppo Locale

Per eseguire i test unitari in locale prima del push:

1.  Crea un environment virtuale:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    pip install pytest
    ```
2.  Lancia i test:
    ```bash
    pytest
    ```