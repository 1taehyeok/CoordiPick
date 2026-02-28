from __future__ import annotations

from fastapi import HTTPException


class AppError(HTTPException):
    def __init__(self, status_code: int, code: str, message: str, details: dict | None = None) -> None:
        super().__init__(
            status_code=status_code,
            detail={
                "code": code,
                "message": message,
                "details": details or {},
            },
        )


class NotFoundError(AppError):
    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(status_code=404, code="NOT_FOUND", message=message, details=details)
