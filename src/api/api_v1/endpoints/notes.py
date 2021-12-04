from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/public-all", response_model=List[schemas.Note])
def get_all_public_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    return crud.get_all_public_notes(db, skip=skip, limit=limit)


@router.get("/public-author", response_model=List[schemas.Note])
def get_public_notes_by_author(
    author: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    db_user = crud.get_user_by_username(db, username=author)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_public_notes_by_author(db, author=author, skip=skip, limit=limit)


@router.get("/public-id", response_model=schemas.Note)
def get_public_note_by_id(
    id: int,
    db: Session = Depends(deps.get_db),
):
    db_note = crud.get_note_by_id(db, id=id)

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    if db_note.public == 0:
        raise HTTPException(status_code=204, detail="Note is not public")

    return db_note


@router.get("/public-search-all", response_model=List[schemas.Note])
def search_all_public_notes(
    text: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):

    return crud.search_all_public_notes(db, text=text, skip=skip, limit=limit)


@router.get("/public-search-author", response_model=List[schemas.Note])
def search_public_notes_by_author(
    text: str,
    author: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    return crud.search_public_notes_by_author(db, text=text, author=author, skip=skip, limit=limit)


@router.get("/search", response_model=List[schemas.Note])
def search_current_user_notes(
    text: str,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    return crud.search_notes_by_author(db, text=text, author=current_user.username, skip=skip, limit=limit)


@router.get("/", response_model=List[schemas.Note])
def get_current_user_notes(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    return crud.get_notes_by_author(db, author=current_user.username, skip=skip, limit=limit)


@router.get("/id", response_model=schemas.Note)
def get_note_by_id(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_note = crud.get_note_by_id(db, id=id)

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    if db_note.author != current_user.username and db_note.public == 0:
        raise HTTPException(status_code=204, detail="Note is not Public")

    return db_note


@router.post("/", response_model=schemas.Note)
def create_note(
    note: schemas.NoteCreate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    return crud.create_note(db, note=note, author=current_user.username)


@router.put("/", response_model=schemas.Note)
def update_note(
    id: int,
    note_update: schemas.NoteUpdate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_note = crud.get_note_by_id(db, id=id)

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    if db_note.author != current_user.username:
        raise HTTPException(status_code=400, detail="Permission denied")

    return crud.update_note(db, id=id, note_update=note_update)


@router.delete("/", response_model=schemas.Note)
def delete_note(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    db_note = crud.get_note_by_id(db, id=id)

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    if db_note.author != current_user.username:
        raise HTTPException(status_code=400, detail="Permission denied")

    return crud.remove_note(db, id=id)
