from fastapi.testclient import TestClient

from src.core.config import settings
from src.tests.utils.user import user_authentication_headers
from src.tests.utils.utils import random_lower_string, username, password, new_username, new_password


def test_get_all_users(client: TestClient):
    response = client.get(
        f"{settings.API_V1_STR}/users/all"
    )
    assert response.status_code == 200


def test_get_user(client: TestClient):
    response = client.get(
        f"{settings.API_V1_STR}/users/",
        headers=user_authentication_headers(
            client=client, u=username, p=password
        )
    )
    user = response.json()
    assert response.status_code == 200
    assert user["username"] == username


def test_update_user(client: TestClient):
    data = {
        "username": new_username,
        "password": new_password,
        "full_name": random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/users/",
        headers=user_authentication_headers(
            client=client, u=username, p=password
        ),
        json=data
    )
    user = response.json()
    assert response.status_code == 200
    assert user["username"] == new_username
    assert user["full_name"] == data["full_name"]


def test_delete_user(client: TestClient):
    response = client.delete(
        f"{settings.API_V1_STR}/users/",
        headers=user_authentication_headers(
            client=client, u=new_username, p=new_password
        ),
    )
    user = response.json()
    assert response.status_code == 200
    assert user["username"] == new_username
