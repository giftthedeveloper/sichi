# Sichi Backend (FastAPI)

## Run

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `GET /api/health`
- `GET /api/profiles?query=amaka`
- `POST /api/profiles`

## Notes

- Storage is in-memory for now (resets on restart).
- Case/message endpoints are intentionally removed for now.
