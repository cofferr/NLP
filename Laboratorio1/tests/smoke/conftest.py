import os

import pytest

EC2_HOST = os.environ.get("EC2_HOST")
LAMBDA_URL = os.environ.get("LAMBDA_URL")

requires_deployed_targets = pytest.mark.skipif(
    not EC2_HOST or not LAMBDA_URL,
    reason="EC2_HOST y LAMBDA_URL deben estar definidas para correr tests de smoke.",
)


def ec2_base_url() -> str:
    host = EC2_HOST.rstrip("/")
    if host.startswith("http://") or host.startswith("https://"):
        return host
    return f"http://{host}:8000"


def lambda_base_url() -> str:
    return LAMBDA_URL.rstrip("/")


@pytest.fixture(scope="session")
def endpoints():
    return {"ec2": ec2_base_url(), "lambda": lambda_base_url()}
