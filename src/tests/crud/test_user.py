from sqlalchemy.orm import Session

from src import crud
from src.core.security import verify_password
from src.schemas.user import UserCreate, UserUpdate
from src.tests.utils.user import create_random_user_by_api
from src.tests.utils.utils import random_lower_string


def test_create_user(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    user_in = UserCreate(username=username, password=password)
    user_obj = crud.create_user(db, user=user_in)

    assert user_obj.username == username
    assert hasattr(user_obj, "hashed_password")


def test_authenticate_user(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    authenticated_user = crud.authenticate_user(
        db,
        username=username,
        password=password
    )

    assert authenticated_user
    assert authenticated_user.username == username


def test_not_authenticate_user(db: Session):
    user = crud.authenticate_user(
        db,
        username=random_lower_string(),
        password=random_lower_string()
    )

    assert user is None


def test_get_all_users(db: Session):
    users = crud. get_users(db)

    assert users


def test_get_user(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    user = crud.get_user_by_username(db, username=username)

    assert user
    assert user.username == username


def test_update_user(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)

    new_username = random_lower_string()
    full_name = random_lower_string()

    user_in_update = UserUpdate(
        username=new_username,
        full_name=full_name,
    )

    crud.update_user(db, username=username, user_update=user_in_update)
    user = crud.get_user_by_username(db, username=new_username)

    assert user
    assert username != new_username
    assert user.full_name


def test_update_password(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)

    new_password = random_lower_string()

    crud.update_password(db, username=username, new_password=new_password)
    user = crud.get_user_by_username(db, username=username)

    assert user
    assert verify_password(new_password, user.hashed_password)


def test_delete_user(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    user = crud.remove_user(db, username=username)

    assert user
    assert user.username == username
