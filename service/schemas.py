"""Pydantic schemas for the FastAPI service."""

from pydantic import BaseModel, ConfigDict


class House(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    bedrooms: int
    grade: int
    last_known_change: int
    center_distance: float


class HouseUpdate(BaseModel):
    bedrooms: int
    grade: int
    last_known_change: int
    center_distance: float
