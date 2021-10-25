from sqlalchemy.orm import Session

from src import crud
from src.models.user import User
from src.schemas.user import UserCreate
from src.tests.utils.utils import username, password


def create_the_random_user(db: Session) -> User:
    user_in = UserCreate(username=username, password=password)
    return crud.create_user(db, user=user_in)


def delete_the_random_user(db: Session) -> User:
    return crud.remove_user(db, username=username)
