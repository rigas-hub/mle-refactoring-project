from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status, Response
from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from service.database import Base, engine, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)

DatabaseSession = Annotated[Session, Depends(get_db)]

class House(BaseModel):
    id: int
    bedrooms: int
    grade: int
    last_known_change: int
    center_distance: float

def get_house_or_404(db: Session, house_id: int) -> House:
    """Return one house or raise the public not-found response."""
    house = db.get(House, house_id)
    if house is None:
        raise HTTPException(status_code=404, detail="House not found")
    return house


@app.get("/", tags=["health"])
def index() -> dict[str, str]:
    """Return a lightweight service status response."""
    return {"status": "ok"}

@app.get("/houses", response_model=list[House])
def get_all_houses(db: DatabaseSession) -> list[House]:
    """Return all persisted houses ordered by identifier."""
    statement = select(House).order_by(House)
    return list(db.scalars(statement))

@app.get("/houses/{house_id}", response_model=House)
def get_house(house_id: int, db: DatabaseSession) -> House:
    """Return one persisted house by identifier."""
    return get_house_or_404(db, house_id)

@app.post("/houses", response_model=House, status_code=status.HTTP_201_CREATED)
def create_house(request: House, db: DatabaseSession) -> House:
    """Persist a new house."""
    new_house = House(id=request.id, bedrooms=request.bedrooms, grade=request.grade, 
                     last_known_change=request.last_known_change, center_distance=request.center_distance)
    db.add(new_house)
    db.commit()
    db.refresh(new_house)
    return new_house

@app.delete("/houses/{house_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_house(house_id: int, db: DatabaseSession) -> Response:
    """Delete one house or return 404 when it does not exist."""
    house = get_house_or_404(db, house_id)

    db.delete(house)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

