from src.tests.conftest import client

from src.core.config import settings
from src.tests.utils.utils import random_lower_string
from src.tests.utils.user import create_random_user_by_api, user_authentication_headers


def test_create_user():
    username = random_lower_string()
    password = random_lower_string()

    data = {
        "username": username,
        "password": password
    }

    response = client.post(
        f"{settings.API_V1_STR}/login/signup",
        json=data
    )

    assert response.status_code == 200


def test_create_existing_user():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)

    data = {
        "username": username,
        "password": password
    }

    response = client.post(
        f"{settings.API_V1_STR}/login/signup",
        json=data
    )

    assert response.status_code == 400


# def test_get_all_users(client: TestClient):
#     response = client.get(
#         f"{settings.API_V1_STR}/users/all"
#     )
#     assert response.status_code == 200


def test_get_user():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    response = client.get(
        f"{settings.API_V1_STR}/users/",
        headers=token,
    )
    user = response.json()

    assert user["username"] == username


def test_update_user():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    data = {
        "username": random_lower_string(),
        "password": random_lower_string(),
        "full_name": random_lower_string()
    }

    response = client.put(
        f"{settings.API_V1_STR}/users/",
        headers=token,
        json=data
    )
    user = response.json()

    assert user["username"] == data["username"]
    assert user["full_name"] == data["full_name"]


def test_delete_user():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    response = client.delete(
        f"{settings.API_V1_STR}/users/",
        headers=token,
    )
    user = response.json()

    assert response.status_code == 200
    assert user["username"] == username
