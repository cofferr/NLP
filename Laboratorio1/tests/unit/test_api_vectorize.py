def test_vectorize_valid_request(client):
    response = client.post("/api/v1/vectorize", json={"documents": ["gato", "perro gato"]})
    assert response.status_code == 200
    data = response.json()
    assert data["vocabulary"] == ["gato", "perro"]
    assert data["bag_of_words"] == [[1, 0], [1, 1]]
    assert data["tf_idf"] == [[1.0, 0.0], [1.0, 1.4055]]


def test_vectorize_rejects_single_document(client):
    response = client.post("/api/v1/vectorize", json={"documents": ["solo un documento"]})
    assert response.status_code >= 400
    assert response.status_code < 500


def test_vectorize_rejects_empty_documents_list(client):
    response = client.post("/api/v1/vectorize", json={"documents": []})
    assert response.status_code >= 400
    assert response.status_code < 500


def test_vectorize_rejects_blank_document(client):
    response = client.post("/api/v1/vectorize", json={"documents": ["texto valido", "   "]})
    assert response.status_code >= 400
    assert response.status_code < 500
