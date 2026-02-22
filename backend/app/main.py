from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.domains.chats.repository import init_chats_tables
from app.domains.profiles.repository import init_profiles_table
from app.domains.transactions.repository import init_transactions_table

app = FastAPI(title="sichi-api", version="0.1.0")


def _cors_allowed_origins() -> list[str]:
    raw = os.getenv("CORS_ALLOWED_ORIGINS", "")
    if not raw.strip():
        return ["http://localhost:5173", "http://127.0.0.1:5173"]
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


@app.on_event("startup")
def startup() -> None:
    init_profiles_table()
    init_chats_tables()
    init_transactions_table()


app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
