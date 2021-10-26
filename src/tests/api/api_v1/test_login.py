from fastapi.testclient import TestClient

from src.core.config import settings
from src.tests.utils.utils import username, password


def test_create_user(client: TestClient):
    data = {"username": username, "password": password}

    response = client.post(
        f"{settings.API_V1_STR}/login/signup", json=data
    )
    assert response.status_code == 200


def test_login(client: TestClient):
    data = {"username": username, "password": password}

    response = client.post(
        f"{settings.API_V1_STR}/login/token", data=data
    )
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
