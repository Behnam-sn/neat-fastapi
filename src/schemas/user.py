from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True
