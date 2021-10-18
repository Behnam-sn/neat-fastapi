from src.database.base import Base
from src.database.session import engine


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
