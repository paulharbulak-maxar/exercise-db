from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from exercise_db.models.models import MuscleGroup
from exercise_db.models.schemas import MuscleGroupCreate, MuscleGroupRead, MuscleRead
from exercise_db.shared.utils.database import engine

router = APIRouter(
    prefix="/muscle_groups",
    tags=["muscle_groups"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=MuscleGroupRead)
def create_muscle_group(muscle_group: MuscleGroupCreate):
    db_muscle_group = MuscleGroup(**muscle_group.model_dump())

    with Session(engine) as session:
        session.add(db_muscle_group)
        session.commit()
        session.refresh(db_muscle_group)
        return db_muscle_group


@router.get("", response_model=list[MuscleGroupRead])
def get_muscle_groups():
    with Session(engine) as session:
        muscle_groups = session.exec(select(MuscleGroup)).all()
        return muscle_groups


@router.get("/{muscle_group_id}", response_model=MuscleGroupRead)
def get_muscle_group(muscle_group_id: int):
    with Session(engine) as session:
        muscle_group = session.get(MuscleGroup, muscle_group_id)

        if muscle_group is None:
            raise HTTPException(status_code=404, detail="Muscle group not found")

        return muscle_group


@router.delete("/{muscle_group_id}", status_code=204)
def delete_muscle_group(muscle_group_id: int):
    with Session(engine) as session:
        muscle_group = session.get(MuscleGroup, muscle_group_id)

        if muscle_group is None:
            raise HTTPException(status_code=404, detail="Muscle group not found")

        session.delete(muscle_group)
        session.commit()


@router.get("/{muscle_group_id}/muscles", response_model=list[MuscleRead])
def get_muscles_by_muscle_group(muscle_group_id: int):
    with Session(engine) as session:
        muscle_group = session.get(MuscleGroup, muscle_group_id)

        if muscle_group is None:
            raise HTTPException(status_code=404, detail="Muscle group not found")

        return muscle_group.muscles
