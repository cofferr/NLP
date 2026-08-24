"""Tests de humo contra los despliegues reales de EC2 y Lambda.

Solo se ejecutan si EC2_HOST y LAMBDA_URL están definidas en el entorno.
Verifican paridad funcional: misma request -> misma respuesta en ambas arquitecturas.
"""

from concurrent.futures import ThreadPoolExecutor

import httpx

from tests.smoke.conftest import requires_deployed_targets

TIMEOUT = 10.0


def _post(base_url: str, path: str, json: dict) -> httpx.Response:
    return httpx.post(f"{base_url}{path}", json=json, timeout=TIMEOUT)


@requires_deployed_targets
def test_clean_parity(endpoints):
    payload = {"text": ["El perro corre", "La casa es grande"]}
    ec2_resp = _post(endpoints["ec2"], "/api/v1/clean", payload)
    lambda_resp = _post(endpoints["lambda"], "/api/v1/clean", payload)

    assert ec2_resp.status_code == 200
    assert lambda_resp.status_code == 200
    assert ec2_resp.json() == lambda_resp.json()


@requires_deployed_targets
def test_pos_parity(endpoints):
    payload = {"text": "El perro corre rápido"}
    ec2_resp = _post(endpoints["ec2"], "/api/v1/pos", payload)
    lambda_resp = _post(endpoints["lambda"], "/api/v1/pos", payload)

    assert ec2_resp.status_code == 200
    assert lambda_resp.status_code == 200
    assert ec2_resp.json() == lambda_resp.json()


@requires_deployed_targets
def test_ner_parity(endpoints):
    payload = {"text": "Juan vive en Madrid"}
    ec2_resp = _post(endpoints["ec2"], "/api/v1/ner", payload)
    lambda_resp = _post(endpoints["lambda"], "/api/v1/ner", payload)

    assert ec2_resp.status_code == 200
    assert lambda_resp.status_code == 200
    assert ec2_resp.json() == lambda_resp.json()


@requires_deployed_targets
def test_vectorize_parity(endpoints):
    payload = {"documents": ["gato", "perro gato"]}
    ec2_resp = _post(endpoints["ec2"], "/api/v1/vectorize", payload)
    lambda_resp = _post(endpoints["lambda"], "/api/v1/vectorize", payload)

    assert ec2_resp.status_code == 200
    assert lambda_resp.status_code == 200
    assert ec2_resp.json() == lambda_resp.json()


@requires_deployed_targets
def test_dep_parity(endpoints):
    payload = {"text": "El perro corre rápido"}
    ec2_resp = _post(endpoints["ec2"], "/api/v1/visualize/dep", payload)
    lambda_resp = _post(endpoints["lambda"], "/api/v1/visualize/dep", payload)

    assert ec2_resp.status_code == 200
    assert lambda_resp.status_code == 200
    assert "<svg" in ec2_resp.text
    assert "<svg" in lambda_resp.text


@requires_deployed_targets
def test_invalid_input_rejected_on_both(endpoints):
    payload = {"text": []}
    ec2_resp = _post(endpoints["ec2"], "/api/v1/clean", payload)
    lambda_resp = _post(endpoints["lambda"], "/api/v1/clean", payload)

    assert 400 <= ec2_resp.status_code < 500
    assert 400 <= lambda_resp.status_code < 500


@requires_deployed_targets
def test_large_batch_within_time_budget(endpoints):
    docs = [f"Documento numero {i} de prueba con texto suficiente." for i in range(25)]
    payload = {"text": docs}

    for base_url in (endpoints["ec2"], endpoints["lambda"]):
        response = _post(base_url, "/api/v1/clean", payload)
        assert response.status_code == 200
        assert response.elapsed.total_seconds() <= TIMEOUT


@requires_deployed_targets
def test_five_concurrent_requests(endpoints):
    def make_request(base_url):
        return _post(base_url, "/api/v1/clean", {"text": "texto de prueba concurrente"})

    targets = [endpoints["ec2"]] * 5

    with ThreadPoolExecutor(max_workers=5) as executor:
        responses = list(executor.map(make_request, targets))

    assert all(r.status_code == 200 for r in responses)
