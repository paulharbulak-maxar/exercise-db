from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from exercise_db.models.models import Muscle, MuscleGroup
from exercise_db.models.schemas import MuscleCreate, MuscleRead
from exercise_db.shared.utils.database import engine

router = APIRouter(
    prefix="/muscles",
    tags=["muscles"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=MuscleRead)
def create_muscle(muscle: MuscleCreate):
    db_muscle = Muscle(**muscle.model_dump())

    with Session(engine) as session:
        session.add(db_muscle)
        session.commit()
        session.refresh(db_muscle)
        return db_muscle


@router.get("", response_model=list[MuscleRead])
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


@router.get("/{muscle_id}", response_model=MuscleRead)
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
