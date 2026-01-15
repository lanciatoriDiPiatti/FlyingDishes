# Flying Dishes

Deploy e test di un'API Flask su Cloud Run.

## Deploy
```bash
gcloud run deploy flying-dishes --source . --platform managed --region europe-west1
```

## Test Locale
```bash
pip install -r requirements.txt
python code/app.py
curl http://localhost:8080/
```

## API
- `GET /` → `{"status": "ok"}`
- `POST /calcola-media` → `{"numeri": [1,2,3]}` → `{"media": 2.0}`
