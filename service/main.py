from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from service import models, schemas
from service.database import Base, engine, get_db


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


def get_house_or_404(db: Session, house_id: int) -> models.House:
    """Return one house or raise the public not-found response."""
    house = db.get(models.House, house_id)
    if house is None:
        raise HTTPException(status_code=404, detail="House not found")
    return house


@app.get("/", tags=["health"])
def index() -> dict[str, str]:
    """Return a lightweight service status response."""
    return {"status": "ok"}


@app.get("/houses", response_model=list[schemas.House])
def get_all_houses(db: Session = Depends(get_db)) -> list[models.House]:
    """Return all persisted houses ordered by identifier."""
    statement = select(models.House).order_by(models.House.id)
    return list(db.scalars(statement))


@app.get("/houses/{house_id}", response_model=schemas.House)
def get_house(house_id: int, db: Session = Depends(get_db)) -> models.House:
    """Return one persisted house by identifier."""
    return get_house_or_404(db, house_id)


@app.post(
    "/houses", response_model=schemas.House, status_code=status.HTTP_201_CREATED
)
def create_house(
    request: schemas.House, db: Session = Depends(get_db)
) -> models.House:
    """Persist a new house."""
    new_house = models.House(**request.model_dump())
    db.add(new_house)
    db.commit()
    db.refresh(new_house)
    return new_house


@app.put("/houses/{house_id}", response_model=schemas.House)
def update_house(
    house_id: int,
    request: schemas.HouseUpdate,
    db: Session = Depends(get_db),
) -> models.House:
    """Replace the editable fields of one house."""
    house = get_house_or_404(db, house_id)

    for field, value in request.model_dump().items():
        setattr(house, field, value)

    db.commit()
    db.refresh(house)
    return house


@app.delete("/houses/{house_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_house(house_id: int, db: Session = Depends(get_db)) -> Response:
    """Delete one house or return 404 when it does not exist."""
    house = get_house_or_404(db, house_id)

    db.delete(house)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
