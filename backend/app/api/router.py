from __future__ import annotations

from fastapi import APIRouter

from app.api.health import router as health_router
from app.domains.chats.router import router as chats_router
from app.domains.profiles.router import router as profiles_router
from app.domains.transactions.router import router as transactions_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router)
api_router.include_router(profiles_router)
api_router.include_router(chats_router)
api_router.include_router(transactions_router)
