# Flying Dishes - Cloud Run Project

## Struttura del Progetto

```
FlyingDishes/
├── code/
│   ├── app.py           # Applicazione Flask (API web)
│   ├── main.py          # Hello World
│   └── media.py         # Versione precedente (CLI)
├── requirements.txt     # Dipendenze Python
├── Dockerfile          # Configurazione container
├── .dockerignore       # File da escludere dal container
└── README.md          # Questo file
```

## Deploy su Cloud Run

### Prerequisiti
- Account Google Cloud
- Google Cloud CLI (`gcloud`) installato
- Progetto Google Cloud creato

### Passi per il Deploy

1. **Autenticati a Google Cloud:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Fai il build e push dell'immagine Docker:**
   ```bash
   gcloud run deploy flying-dishes \
     --source . \
     --platform managed \
     --region europe-west1 \
     --allow-unauthenticated
   ```

3. **Usa l'API:**
   ```bash
   curl https://flying-dishes-xxxxx.a.run.app/
   
   curl -X POST https://flying-dishes-xxxxx.a.run.app/calcola-media \
     -H "Content-Type: application/json" \
     -d '{"numeri": [10, 20, 30, 40, 50]}'
   ```

## Test Locale

```bash
pip install -r requirements.txt
python code/app.py
# Accedi a http://localhost:8080
```

## API Endpoints

### POST `/calcola-media`
Calcola la media dei numeri forniti

**Request:** `{"numeri": [1, 2, 3, 4, 5]}`
**Response:** `{"numeri": [...], "media": 3.0, "quantita": 5}`
