# Usa immagine Python ufficiale
FROM python:3.11-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia requirements.txt e installa dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY code/app.py .

# Esponi la porta 8080 (standard per Cloud Run)
EXPOSE 8080

# Comando per avviare l'app
CMD ["python", "app.py"]
