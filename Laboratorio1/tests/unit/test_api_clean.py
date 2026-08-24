def test_clean_single_string_returns_list(client):
    response = client.post("/api/v1/clean", json={"text": "El perro corre"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["cleaned_text"], list)
    assert len(data["cleaned_text"]) == 1


def test_clean_batch_preserves_order(client):
    response = client.post("/api/v1/clean", json={"text": ["Hola mundo", "Buenos días"]})
    assert response.status_code == 200
    data = response.json()
    assert len(data["cleaned_text"]) == 2


def test_clean_rejects_empty_list(client):
    response = client.post("/api/v1/clean", json={"text": []})
    assert response.status_code >= 400
    assert response.status_code < 500


def test_clean_rejects_empty_string(client):
    response = client.post("/api/v1/clean", json={"text": "   "})
    assert response.status_code >= 400
    assert response.status_code < 500


def test_clean_rejects_non_string_elements(client):
    response = client.post("/api/v1/clean", json={"text": ["hola", 123]})
    assert response.status_code >= 400
    assert response.status_code < 500


def test_clean_rejects_missing_field(client):
    response = client.post("/api/v1/clean", json={})
    assert response.status_code >= 400
    assert response.status_code < 500


def test_clean_rejects_null(client):
    response = client.post("/api/v1/clean", json={"text": None})
    assert response.status_code >= 400
    assert response.status_code < 500
