from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src import crud
from src.models.user import User
from src.schemas.user import UserCreate
from src.core.config import settings
from src.tests.utils.utils import username, password


def create_the_random_user(db: Session) -> User:
    user_in = UserCreate(username=username, password=password)
    return crud.create_user(db, user=user_in)


def delete_the_random_user(db: Session) -> User:
    return crud.remove_user(db, username=username)


def user_authentication_headers(client: TestClient, u, p):
    data = {"username": u, "password": p}

    response = client.post(
        f"{settings.API_V1_STR}/login/token", data=data
    )
    tokens = response.json()
    auth_token = tokens["access_token"]
    return {"Authorization": f"Bearer {auth_token}"}
