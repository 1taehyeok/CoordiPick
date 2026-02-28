from __future__ import annotations


def test_create_event(test_client):
    response = test_client.post(
        "/api/v1/events",
        json={
            "session_id": "session-3",
            "event_type": "click",
            "recommendation_id": "rec_session-3_1",
            "payload": {"position": 1},
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert "event_id" in body["data"]


def test_create_event_validation_error(test_client):
    response = test_client.post(
        "/api/v1/events",
        json={
            "session_id": "session-4",
            "event_type": "unknown",
            "recommendation_id": "rec_session-4_1",
        },
    )
    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "INVALID_INPUT"
