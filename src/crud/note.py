import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from src import models, schemas


def create_note(db: Session, note: schemas.NoteCreate, author: str) -> models.Note:
    db_note = models.Note(
        **note.dict(),
        author=author,
        created_at=datetime.datetime.now(),
        modified_at=datetime.datetime.now(),
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_all_public_notes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Note]:
    return (
        db.query(models.Note)
        .filter(models.Note.public == 1)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_public_notes_by_author(db: Session, author: str, skip: int = 0, limit: int = 100) -> List[models.Note]:
    return (
        db.query(models.Note)
        .filter(models.Note.author == author, models.Note.public == 1)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_notes_by_author(db: Session, author: str, skip: int = 0, limit: int = 100) -> List[models.Note]:
    return (
        db.query(models.Note)
        .filter(models.Note.author == author)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_note_by_id(db: Session, id: int) -> Optional[models.Note]:
    return (
        db.query(models.Note)
        .filter(models.Note.id == id)
        .first()
    )


def update_note(db: Session, id: int, note_update: schemas.NoteUpdate) -> models.Note:
    db_note = get_note_by_id(db, id=id)

    update_data = note_update.dict(exclude_unset=True)
    update_data["modified_at"] = datetime.datetime.now()

    for field, value in update_data.items():
        setattr(db_note, field, value)

    db.commit()
    db.refresh(db_note)
    return db_note


def remove_note(db: Session, id: int) -> models.Note:
    db_note = get_note_by_id(db, id=id)
    db.delete(db_note)
    db.commit()
    return db_note
