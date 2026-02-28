from __future__ import annotations

from fastapi import APIRouter

from app.api.routes import events, recommendations

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(recommendations.router)
api_router.include_router(events.router)
