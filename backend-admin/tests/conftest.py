import pytest
from fastapi.testclient import TestClient

from app.dependencies import reset_dependencies
from app.main import app


@pytest.fixture(autouse=True)
def _reset_state() -> None:
    reset_dependencies()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer test-token"}
