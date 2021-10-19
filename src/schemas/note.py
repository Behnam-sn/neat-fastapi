from typing import Optional

from pydantic import BaseModel


# Shared properties
class NoteBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# Properties to receive on Note creation
class NoteCreate(NoteBase):
    title: str


# Properties to receive on Note update
class NoteUpdate(NoteBase):
    pass


# Properties shared by models stored in DB
class NoteInDBBase(NoteBase):
    id: int
    title: str
    author: int

    class Config:
        orm_mode = True


# Properties to return to client
class Note(NoteInDBBase):
    pass


# Properties properties stored in DB
class NoteInDB(NoteInDBBase):
    pass
