from fastapi import APIRouter
from sqlmodel import Session, select

from models.models import MuscleGroup, MuscleGroupResponse
from shared.utils.database import engine

router = APIRouter(
    prefix="/muscle_groups",
    tags=["muscle_groups"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=MuscleGroupResponse)
def create_muscle_group(muscle_group: MuscleGroup):
    with Session(engine) as session:
        session.add(muscle_group)
        session.commit()
        session.refresh(muscle_group)
        return muscle_group


@router.get("/", response_model=list[MuscleGroupResponse])
def get_muscle_groups():
    with Session(engine) as session:
        muscle_groups = session.exec(select(MuscleGroup)).all()
        return muscle_groups
