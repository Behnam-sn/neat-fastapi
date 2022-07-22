from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True, index=True)
    created_at = Column(Text)
    modified_at = Column(Text)

    notes = relationship("Note", back_populates="author_id")
