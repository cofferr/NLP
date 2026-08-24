def test_pos_single_text(client):
    response = client.post("/api/v1/pos", json={"text": "El perro corre"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    tokens = data["results"][0]["tokens"]
    assert all({"text", "pos", "lemma"} <= set(t.keys()) for t in tokens)


def test_pos_batch_preserves_order_and_correspondence(client):
    texts = ["El gato duerme", "Los niños juegan"]
    response = client.post("/api/v1/pos", json={"text": texts})
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 2
    first_tokens = [t["text"] for t in data["results"][0]["tokens"]]
    second_tokens = [t["text"] for t in data["results"][1]["tokens"]]
    assert "gato" in first_tokens
    assert "niños" in second_tokens


def test_pos_rejects_invalid_input(client):
    response = client.post("/api/v1/pos", json={"text": [""]})
    assert response.status_code >= 400
    assert response.status_code < 500
