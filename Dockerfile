# Usa un'immagine base di Python leggera
FROM python:3.9-slim

# Imposta la cartella di lavoro nel container
WORKDIR /app

# Copia i requisiti e installali
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'app e il modello
COPY app.py .
COPY sentimentanalysismodel.pkl .

# Espone la porta 5000 (quella di Flask)
EXPOSE 5000

# Comando per avviare l'app
CMD ["python", "app.py"]