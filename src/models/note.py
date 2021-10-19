from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from src.database.base_class import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text, index=True)
    author = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime(timezone=True))
    modified_at = Column(DateTime(timezone=True))

    owner = relationship("User", back_populates="notes")
