from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Note])
def get_public_notes(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud.get_public_notes(db, skip=skip, limit=limit)


@router.get("/{author}", response_model=List[schemas.Note])
def get_notes_by_author(
    author: str,
    db: Session = Depends(deps.get_db),
):
    pass


@router.get("/{id}", response_model=schemas.Note)
def get_note_by_id(
    id: int,
    db: Session = Depends(deps.get_db),
):
    pass
