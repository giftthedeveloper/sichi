# Sichi Backend (FastAPI)

## Run

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Notebook: Local Mistral Connectivity Test

Prerequisite (outside Python):

```bash
ollama pull mistral
ollama run mistral
```

In another terminal:

```bash
cd backend
source .venv/bin/activate
pip install -r requirements-notebook.txt
jupyter lab notebooks/sichi_rag_playground.ipynb
```

The notebook sends one prompt to `http://localhost:11434` and prints the response to confirm local connection.

## Structure

- `app/core` shared infrastructure (db connection)
- `app/domains/profiles` profile domain (models/repository/service/schemas/router)
- `app/domains/chats` chat domain (models/repository/service/schemas/router)
- `app/domains/transactions` transaction domain (models/repository/service/schemas/router)
- `app/api` shared API router + health route

## Endpoints

- `GET /api/health`
- `GET /api/profiles?query=amaka`
- `POST /api/profiles`
- `POST /api/chats/session`
- `GET /api/chats/{chat_id}?cursor=123&limit=20`
- `POST /api/chats/{chat_id}/messages`
- `GET /api/transactions?page=1&page_size=5`
- `POST /api/transactions`

## Notes

- Uses SQLite file storage at `backend/sichi.db`.
- No seed profiles are inserted on startup.
