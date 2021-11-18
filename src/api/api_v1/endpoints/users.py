from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/all", response_model=List[schemas.User])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/", response_model=schemas.User)
def get_user(
    # current_user: models.User = Depends(deps.get_current_user),
    username: str,
    db: Session = Depends(deps.get_db),
):
    db_user = crud.get_user_by_username(db, username=username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.put("/", response_model=schemas.User)
def update_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    db_user = crud.get_user_by_username(db, username=current_user.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.username != user_update.username:
        new_name = crud.get_user_by_username(db, username=user_update.username)

        if new_name:
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )

    return crud.update_user(db, username=current_user.username, user_update=user_update)


@router.delete("/", response_model=schemas.User)
def delete_user(
    password: str,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    db_user = crud.get_user_by_username(db, username=current_user.username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if crud.authenticate_user(db, username=current_user.username, password=password) is None:
        raise HTTPException(
            status_code=400,
            detail="Not Authenticated"
        )

    return crud.remove_user(db, username=current_user.username)
