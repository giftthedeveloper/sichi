# Sichi Backend (FastAPI)

## Run

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Structure

- `app/core` shared infrastructure (db connection)
- `app/domains/profiles` profile domain (models/repository/service/schemas/router)
- `app/api` shared API router + health route

## Endpoints

- `GET /api/health`
- `GET /api/profiles?query=amaka`
- `POST /api/profiles`

## Notes

- Uses SQLite file storage at `backend/sichi.db`.
- No seed profiles are inserted on startup.
