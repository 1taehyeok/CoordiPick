from fastapi import FastAPI

from app.api.routes.admin import router as admin_router
from app.core.errors import install_error_handlers

app = FastAPI(title="CoordiPick Admin API", version="0.1.0")
install_error_handlers(app)
app.include_router(admin_router, prefix="/api/v1")
