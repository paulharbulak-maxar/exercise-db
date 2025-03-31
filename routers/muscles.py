from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.models import Muscle, MuscleResponse
from shared.utils.database import engine

router = APIRouter(
    prefix="/muscles",
    tags=["muscles"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=MuscleResponse)
def create_muscle(muscle: Muscle):
    with Session(engine) as session:
        session.add(muscle)
        session.commit()
        session.refresh(muscle)
        return muscle


# TODO: Add muscle group name query filter
@router.get("", response_model=list[MuscleResponse])
def get_muscles():
    with Session(engine) as session:
        muscles = session.exec(select(Muscle)).all()
        return muscles


@router.get("/{muscle_id}", response_model=MuscleResponse)
def get_muscle(muscle_id: int):
    with Session(engine) as session:
        muscle = session.exec(select(Muscle).where(Muscle.id == muscle_id)).first()

        if muscle is None:
            raise HTTPException(status_code=404, detail="Muscle not found")

        return muscle


# TODO: Create route for delete
