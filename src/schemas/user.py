from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str
    full_name: str


class PasswordUpdate(BaseModel):
    password: str
    new_password: str


class User(UserBase):
    id: int
    created_at: str
    modified_at: str

    class Config:
        orm_mode = True
