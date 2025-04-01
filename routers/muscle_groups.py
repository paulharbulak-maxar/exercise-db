from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.models import MuscleGroup, MuscleGroupResponse, MuscleResponse
from shared.utils.database import engine

router = APIRouter(
    prefix="/muscle_groups",
    tags=["muscle_groups"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=MuscleGroupResponse)
def create_muscle_group(muscle_group: MuscleGroup):
    with Session(engine) as session:
        session.add(muscle_group)
        session.commit()
        session.refresh(muscle_group)
        return muscle_group


@router.get("", response_model=list[MuscleGroupResponse])
def get_muscle_groups():
    with Session(engine) as session:
        muscle_groups = session.exec(select(MuscleGroup)).all()
        return muscle_groups


@router.get("/{muscle_group_id}", response_model=MuscleGroupResponse)
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


@router.get("/{muscle_group_id}/muscles", response_model=list[MuscleResponse])
def get_muscles_by_muscle_group(muscle_group_id: int):
    with Session(engine) as session:
        muscle_group = session.get(MuscleGroup, muscle_group_id)

        if muscle_group is None:
            raise HTTPException(status_code=404, detail="Muscle group not found")

        return muscle_group.muscles
