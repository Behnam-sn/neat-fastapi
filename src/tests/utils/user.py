from src.tests.conftest import client

from src.core.config import settings


def create_random_user_by_api(username: str, password: str):
    data = {"username": username, "password": password}

    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=data
    )


def user_authentication_headers(username: str, password: str):
    data = {"username": username, "password": password}

    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=data
    )
    tokens = response.json()
    auth_token = tokens["access_token"]

    return {"Authorization": f"Bearer {auth_token}"}
