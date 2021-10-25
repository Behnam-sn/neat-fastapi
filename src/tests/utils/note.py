from sqlalchemy.orm import Session

from src import crud
from src.models.note import Note
from src.schemas.note import NoteCreate
from src.tests.utils.utils import random_lower_string


def creat_random_note(db: Session, public: bool, author: str) -> Note:
    title = random_lower_string()
    content = random_lower_string()
    note_in = NoteCreate(title=title, content=content, public=public)
    return crud.create_note(db, note=note_in, author=author)
