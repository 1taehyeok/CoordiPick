def _item_payload() -> dict:
    return {
        "category": "tops",
        "sub_category": "shirt",
        "gender": "unisex",
        "fit": "regular",
        "color_tone": "neutral",
        "moods": ["minimal"],
        "tpos": ["daily"],
        "temperature_min": 10,
        "temperature_max": 24,
        "price_krw": 39000,
        "stock_qty": 7,
        "image_url": "https://example.com/item.jpg",
        "location_zone": "A-1",
        "is_active": True,
    }


def test_auth_required(client):
    response = client.get("/api/v1/admin/items")
    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False
    assert "error" in body


def test_item_crud_flow(client, auth_headers):
    create_response = client.post("/api/v1/admin/items", headers=auth_headers, json=_item_payload())
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["success"] is True
    item_id = created["data"]["item_id"]

    list_response = client.get("/api/v1/admin/items", headers=auth_headers)
    assert list_response.status_code == 200
    assert len(list_response.json()["data"]["items"]) == 1

    update_response = client.patch(
        f"/api/v1/admin/items/{item_id}",
        headers=auth_headers,
        json={"stock_qty": 3},
    )
    assert update_response.status_code == 200
    assert update_response.json()["data"]["stock_qty"] == 3

    delete_response = client.delete(f"/api/v1/admin/items/{item_id}", headers=auth_headers)
    assert delete_response.status_code == 204
    assert delete_response.content == b""


def test_outfit_requires_existing_item(client, auth_headers):
    response = client.post(
        "/api/v1/admin/outfits",
        headers=auth_headers,
        json={
            "title": "Daily look",
            "subtitle": "simple",
            "gender_target": "unisex",
            "tpo": "daily",
            "mood": "minimal",
            "total_price_krw": 50000,
            "generation_source": "admin",
            "score": 0.9,
            "created_by": "admin",
            "items": [{"item_id": "999", "slot": "top", "sort_order": 0}],
        },
    )
    assert response.status_code == 400
    assert response.json()["success"] is False


def test_outfit_update_flow(client, auth_headers):
    client.post("/api/v1/admin/items", headers=auth_headers, json=_item_payload())
    create_response = client.post(
        "/api/v1/admin/outfits",
        headers=auth_headers,
        json={
            "title": "Daily look",
            "subtitle": "simple",
            "gender_target": "unisex",
            "tpo": "daily",
            "mood": "minimal",
            "total_price_krw": 50000,
            "generation_source": "admin",
            "score": 0.9,
            "created_by": "admin",
            "items": [{"item_id": "1", "slot": "top", "sort_order": 0}],
        },
    )
    outfit_id = create_response.json()["data"]["outfit_id"]

    update_response = client.patch(
        f"/api/v1/admin/outfits/{outfit_id}",
        headers=auth_headers,
        json={"title": "Updated look", "items": [{"item_id": "1", "slot": "top", "sort_order": 0}]},
    )
    assert update_response.status_code == 200
    assert update_response.json()["data"]["title"] == "Updated look"


def test_store_settings_get_and_patch(client, auth_headers):
    get_response = client.get("/api/v1/admin/store-settings", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json()["data"]["store_id"] == "default"

    patch_response = client.patch(
        "/api/v1/admin/store-settings",
        headers=auth_headers,
        json={
            "target_gender": "female",
            "price_band_min_krw": 30000,
            "price_band_max_krw": 120000,
            "mood_weights": {"minimal": 1.2},
        },
    )
    assert patch_response.status_code == 200
    body = patch_response.json()
    assert body["success"] is True
    assert body["data"]["target_gender"] == "female"


def test_dashboard_endpoints(client, auth_headers):
    client.post("/api/v1/admin/items", headers=auth_headers, json={**_item_payload(), "stock_qty": 2})
    client.post(
        "/api/v1/admin/items",
        headers=auth_headers,
        json={**_item_payload(), "sub_category": "pants", "tpos": ["commute"], "stock_qty": 8},
    )
    outfit_response = client.post(
        "/api/v1/admin/outfits",
        headers=auth_headers,
        json={
            "title": "Commuter",
            "subtitle": None,
            "gender_target": "unisex",
            "tpo": "commute",
            "mood": "smart",
            "total_price_krw": 89000,
            "generation_source": "admin",
            "score": 0.75,
            "created_by": "admin",
            "items": [{"item_id": "1", "slot": "top", "sort_order": 0}],
        },
    )
    assert outfit_response.status_code == 201

    summary = client.get("/api/v1/admin/dashboard/summary", headers=auth_headers)
    assert summary.status_code == 200
    assert summary.json()["data"]["items_total"] == 2
    assert summary.json()["data"]["outfits_total"] == 1

    top3 = client.get("/api/v1/admin/dashboard/top3", headers=auth_headers)
    assert top3.status_code == 200
    assert len(top3.json()["data"]["outfits"]) == 1

    tpo_ratio = client.get("/api/v1/admin/dashboard/tpo-ratio", headers=auth_headers)
    assert tpo_ratio.status_code == 200
    assert tpo_ratio.json()["data"]["tpo_ratio"]["commute"] == 1.0

    low_stock = client.get("/api/v1/admin/dashboard/low-stock", headers=auth_headers)
    assert low_stock.status_code == 200
    assert low_stock.json()["data"]["items"][0]["stock_qty"] == 2
