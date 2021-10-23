from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class NoteBase(BaseModel):
    title: Optional[str] = None
    content: str
    public: bool


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    public: Optional[bool] = None


class Note(NoteBase):
    id: int
    author: str
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True
