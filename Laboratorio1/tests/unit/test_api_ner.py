def test_ner_single_text(client):
    response = client.post("/api/v1/ner", json={"text": "Juan vive en Madrid"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    entities = data["results"][0]["entities"]
    for ent in entities:
        assert {"text", "label", "start", "end"} <= set(ent.keys())


def test_ner_batch_preserves_order(client):
    texts = ["Juan vive en Madrid", "María trabaja en Barcelona"]
    response = client.post("/api/v1/ner", json={"text": texts})
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 2


def test_ner_rejects_batch_with_blank_text(client):
    response = client.post("/api/v1/ner", json={"text": ["Juan vive en Madrid", "   "]})
    assert response.status_code >= 400
    assert response.status_code < 500
