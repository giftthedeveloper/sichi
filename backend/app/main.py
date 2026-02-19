from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.domains.chats.repository import init_chats_tables
from app.domains.profiles.repository import init_profiles_table
from app.domains.transactions.repository import init_transactions_table

app = FastAPI(title="sichi-api", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    init_profiles_table()
    init_chats_tables()
    init_transactions_table()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
