from __future__ import annotations

from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)
