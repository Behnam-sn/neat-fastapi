from src.tests.conftest import client

from src.core.config import settings
from src.tests.utils.utils import random_lower_string
from src.tests.utils.user import create_random_user_by_api


def test_login():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)

    data = {
        "username": username,
        "password": password
    }

    response = client.post(
        f"{settings.API_V1_STR}/login/token",
        data=data
    )
    tokens = response.json()

    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
