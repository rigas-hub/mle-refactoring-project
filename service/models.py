"""SQLAlchemy models for the FastAPI service."""

from sqlalchemy import Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from service.database import Base


class House(Base):
    __tablename__ = "houses"

    id: Mapped[int] = mapped_column(primary_key=True)
    bedrooms: Mapped[int] = mapped_column(Integer)
    grade: Mapped[int] = mapped_column(Integer)
    last_known_change: Mapped[int] = mapped_column(Integer)
    center_distance: Mapped[float] = mapped_column(Float)
