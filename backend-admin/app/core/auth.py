from fastapi import Header

from app.core.errors import ApiError


def require_admin_bearer(authorization: str | None = Header(default=None)) -> str:
    if not authorization:
        raise ApiError(code="UNAUTHORIZED", message="missing bearer token", status_code=401)

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise ApiError(code="UNAUTHORIZED", message="invalid bearer token", status_code=401)

    return token
