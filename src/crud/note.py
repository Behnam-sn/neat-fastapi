from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import true

from src.models.note import Note
from src.schemas.note import NoteCreate, NoteUpdate


def create_note(db: Session, obj_in: NoteCreate, author: str) -> Note:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Note(**obj_in_data, author=author)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


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


def get_notes_by_public(db: Session, skip: int = 0, limit: int = 100) -> List[Note]:
    return (
        db.query(Note)
        .filter(Note.public == true)
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
