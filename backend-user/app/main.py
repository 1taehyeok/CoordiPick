from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.router import api_router

app = FastAPI(title="CoordiPick User API", version="0.1.0")
app.include_router(api_router)


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "validation failed",
                "details": {"errors": exc.errors()},
            },
        },
    )


@app.exception_handler(HTTPException)
async def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail if isinstance(exc.detail, dict) else {"code": "HTTP_ERROR", "message": str(exc.detail), "details": {}}
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": detail.get("code", "HTTP_ERROR"),
                "message": detail.get("message", "request failed"),
                "details": detail.get("details", {}),
            },
        },
    )
