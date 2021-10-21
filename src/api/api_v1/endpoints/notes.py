from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Note)
def create_note(
    note: schemas.NoteCreate,
    author: str,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    if author != current_user.username:
        raise HTTPException(status_code=400, detail="permission denied")

    return crud.create_note(db, note=note, author=author)


@router.get("/", response_model=List[schemas.Note])
def get_public_notes(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud.get_public_notes(db, skip=skip, limit=limit)


@router.get("/{author}", response_model=List[schemas.Note])
def get_notes_by_author(
    author: str,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    if author == current_user.username:
        notes = []
    else:
        notes = ""

    return notes


@router.get("/{id}", response_model=schemas.Note)
def get_note_by_id():
    pass


@router.put("/{id}", response_model=schemas.Note)
def update_note():
    pass


@router.delete("/{id}", response_model=schemas.Note)
def delete_note():
    pass
