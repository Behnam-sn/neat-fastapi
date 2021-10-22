from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship

from src.database.session import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text, index=True)
    public = Column(Boolean, index=True)
    author = Column(String, ForeignKey("users.username"))
    created_at = Column(DateTime(timezone=True))
    modified_at = Column(DateTime(timezone=True))

    author_id = relationship("User", back_populates="notes")
