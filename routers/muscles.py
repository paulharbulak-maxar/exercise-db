from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.models import Muscle, MuscleGroup, MuscleResponse
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


@router.get("", response_model=list[MuscleResponse])
def get_muscles(muscle_group: str = None):
    with Session(engine) as session:
        query = select(Muscle)
        if muscle_group:
            muscle_group_result = session.exec(
                select(MuscleGroup).where(MuscleGroup.name == muscle_group)
            ).first()

            query = query.where(Muscle.muscle_group == muscle_group_result)

        muscles = session.exec(query).all()
        return muscles


@router.get("/{muscle_id}", response_model=MuscleResponse)
def get_muscle(muscle_id: int):
    with Session(engine) as session:
        muscle = session.get(Muscle, muscle_id)

        if muscle is None:
            raise HTTPException(status_code=404, detail="Muscle not found")

        return muscle


@router.delete("/{muscle_id}", status_code=204)
def delete_muscle(muscle_id: int):
    with Session(engine) as session:
        muscle = session.get(Muscle, muscle_id)

        if muscle is None:
            raise HTTPException(status_code=404, detail="Muscle not found")

        session.delete(muscle)
        session.commit()
