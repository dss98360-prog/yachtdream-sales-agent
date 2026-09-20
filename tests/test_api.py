def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qualification_saves_lead(client, valid_lead):
    response = client.post("/api/qualify", json=valid_lead)
    assert response.status_code == 201
    body = response.json()
    assert body["lead_id"] == 1
    assert body["recommendation"]["program_id"] == "bareboat"

    admin = client.get("/api/admin/leads", headers={"X-Admin-Key": "test-admin-key"})
    assert admin.status_code == 200
    assert admin.json()["total"] == 1
    assert admin.json()["items"][0]["name"] == "Алексей"


def test_admin_requires_key(client):
    response = client.get("/api/admin/leads")
    assert response.status_code == 401


def test_rejects_invalid_email(client, valid_lead):
    valid_lead["email"] = "not-an-email"
    response = client.post("/api/qualify", json=valid_lead)
    assert response.status_code == 422


def test_updates_lead_status(client, valid_lead):
    client.post("/api/qualify", json=valid_lead)
    response = client.patch(
        "/api/admin/leads/1",
        headers={"X-Admin-Key": "test-admin-key"},
        json={"status": "contacted"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "contacted"

