from __future__ import annotations


def test_generate_recommendations_schema(test_client):
    response = test_client.post(
        "/api/v1/recommendations/generate",
        json={
            "session_id": "session-1",
            "gender": "male",
            "tpo": "commute",
            "mood": "clean",
            "temperature_c": 17,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "data" in body and "cards" in body["data"]
    assert 1 <= len(body["data"]["cards"]) <= 6

    card = body["data"]["cards"][0]
    assert set(card.keys()).issuperset({"recommendation_id", "title", "total_price_krw", "thumbnail_url"})
    assert "meta" in body and "generated_at" in body["meta"]


def test_get_recommendation_detail(test_client):
    generated = test_client.post(
        "/api/v1/recommendations/generate",
        json={
            "session_id": "session-2",
            "gender": "female",
            "tpo": "date",
            "mood": "romantic",
            "temperature_c": 14,
        },
    )
    recommendation_id = generated.json()["data"]["cards"][0]["recommendation_id"]

    response = test_client.get(f"/api/v1/recommendations/{recommendation_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["recommendation_id"] == recommendation_id
    assert isinstance(body["data"]["items"], list)
    assert all("slot" in item for item in body["data"]["items"])


def test_recommendation_not_found(test_client):
    response = test_client.get("/api/v1/recommendations/does-not-exist")
    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "NOT_FOUND"
