from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import true

from src.models.note import Note
from src.schemas.note import NoteCreate, NoteUpdate


def create_note(db: Session, note: NoteCreate, author: str) -> Note:
    db_note = Note(**note, author=author)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_note_by_id(db: Session, id: int) -> Optional[Note]:
    return db.query(Note).filter(Note.id == id).first()


def get_notes_by_author(db: Session, author: str, skip: int = 0, limit: int = 100) -> List[Note]:
    return (
        db.query(Note)
        .filter(Note.author == author)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_public_notes(db: Session, skip: int = 0, limit: int = 100) -> List[Note]:
    return (
        db.query(Note)
        .filter(Note.public == 1)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_note():
    pass


def remove_note(db: Session, id: int) -> Note:
    note = get_note_by_id(db, id=id)
    db.delete(note)
    db.commit()
    return note
