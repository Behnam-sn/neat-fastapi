from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text
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
    public = Column(Boolean, index=True)

    author_id = relationship("User", back_populates="notes")
