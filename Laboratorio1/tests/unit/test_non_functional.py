from concurrent.futures import ThreadPoolExecutor


def test_handles_large_batch_clean_pos_ner(client):
    docs = [f"Este es el documento numero {i} con algo de texto de prueba." for i in range(25)]
    for endpoint in ("/api/v1/clean", "/api/v1/pos", "/api/v1/ner"):
        response = client.post(endpoint, json={"text": docs})
        assert response.status_code == 200


def test_handles_large_batch_vectorize(client):
    docs = [f"Documento numero {i} para vectorizar con texto de prueba." for i in range(10)]
    response = client.post("/api/v1/vectorize", json={"documents": docs})
    assert response.status_code == 200


def test_handles_five_concurrent_requests(client):
    def make_request(i):
        return client.post("/api/v1/clean", json={"text": f"texto de prueba numero {i}"})

    with ThreadPoolExecutor(max_workers=5) as executor:
        responses = list(executor.map(make_request, range(5)))

    assert all(r.status_code == 200 for r in responses)


def test_requests_do_not_share_state():
    """Dos requests equivalentes deben producir la misma salida, sin importar el orden de ejecución."""
    from fastapi.testclient import TestClient
    from app.main import app

    local_client = TestClient(app)
    first = local_client.post("/api/v1/clean", json={"text": "El perro corre"})
    second = local_client.post("/api/v1/clean", json={"text": "El perro corre"})
    assert first.json() == second.json()
