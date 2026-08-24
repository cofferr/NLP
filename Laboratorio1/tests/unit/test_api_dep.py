def test_dep_returns_html_svg(client):
    response = client.post("/api/v1/visualize/dep", json={"text": "El perro corre rápido"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<svg" in response.text


def test_dep_rejects_list_input(client):
    response = client.post("/api/v1/visualize/dep", json={"text": ["uno", "dos"]})
    assert response.status_code >= 400
    assert response.status_code < 500


def test_dep_rejects_empty_text(client):
    response = client.post("/api/v1/visualize/dep", json={"text": "   "})
    assert response.status_code >= 400
    assert response.status_code < 500
