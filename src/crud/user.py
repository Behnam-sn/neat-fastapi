import datetime
from typing import Optional

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from src.core.security import get_password_hash, verify_password
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        created_at=datetime.datetime.now(),
        modified_at=datetime.datetime.now(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, username: str, user: UserUpdate) -> User:
    db_user = db.query(User).filter(User.username == username)
    stored_user_model = User(**db_user.first())
    update_data = user.dict(exclude_unset=True)

    if update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password

    update_data["modified_at"] = datetime.datetime.now()

    updated_user = stored_user_model.copy(update=update_data)

    db_user.update(jsonable_encoder(updated_user), synchronize_session=False)
    db.commit()
    db.refresh(db_user)
    return db_user


# def update_user(db: Session, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
#     obj_data = jsonable_encoder(db_obj)

#     if isinstance(obj_in, dict):
#         update_data = obj_in
#     else:
#         update_data = obj_in.dict(exclude_unset=True)

#     if update_data["password"]:
#         hashed_password = get_password_hash(update_data["password"])
#         del update_data["password"]
#         update_data["hashed_password"] = hashed_password

#     for field in obj_data:
#         if field in update_data:
#             setattr(db_obj, field, update_data[field])

#     db.add(db_obj)
#     db.commit()
#     db.refresh(db_obj)
#     return db_obj


def remove_user(db: Session, username: str) -> User:
    user = get_user_by_username(db, username=username)
    db.delete(user)
    db.commit()
    return user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username=username)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
