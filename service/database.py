from collections.abc import Generator
from pathlib import Path

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_PATH = Path(__file__).resolve().with_name("houses.db")
DATABASE_URL = URL.create("sqlite", database=str(DATABASE_PATH))
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Base class shared by the service's SQLAlchemy models."""


def get_db() -> Generator[Session]:
    """Yield one database session for a request, then close it."""
    with SessionLocal() as session:
        yield session
