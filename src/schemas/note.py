from typing import Optional

from pydantic import BaseModel


class NoteBase(BaseModel):
    title: Optional[str] = None
    content: str
    public: bool


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    author: str
    created_at: str
    modified_at: str

    class Config:
        orm_mode = True
