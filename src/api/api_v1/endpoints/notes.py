from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Note)
def create_note(
    note: schemas.NoteCreate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):

    return crud.create_note(db, note=note, author=current_user.username)


@router.get("/public", response_model=List[schemas.Note])
def get_public_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):

    return crud.get_public_notes(db, skip=skip, limit=limit)


@router.get("/", response_model=List[schemas.Note])
def get_user_notes(
    current_user: Optional[models.User] = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):

    return crud.get_currnet_user_notes(db, author=current_user.username)


@router.get("/author", response_model=List[schemas.Note])
def get_notes_by_author(
    author: str,
    db: Session = Depends(deps.get_db),
):

    return crud.get_notes_by_author(db, author=author)


@router.get("/id", response_model=schemas.Note)
def get_note_by_id(
    id: int,
    db: Session = Depends(deps.get_db),
):

    return crud.get_note_by_id(db, id=id)


@router.put("/", response_model=schemas.Note)
def update_note(
    note: schemas.Note,
    note_update: schemas.NoteUpdate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):

    if current_user.username != note.author:
        raise HTTPException(status_code=400, detail="Permission denied")

    db_note = crud.get_note_by_id(db, id=note.id)

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return crud.update_note(db, id=note.id, note_update=note_update)


@router.delete("/", response_model=schemas.Note)
def delete_note(
    note: schemas.Note,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):

    if current_user.username != note.author:
        raise HTTPException(status_code=400, detail="Permission denied")

    db_note = crud.get_note_by_id(db, id=note.id)

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return crud.remove_note(db, id=note.id)
