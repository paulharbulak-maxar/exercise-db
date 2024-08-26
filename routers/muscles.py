from fastapi import APIRouter
from sqlmodel import Session, select

from models.exercise import Exercise
from models.muscle import Muscle
from models.muscle_group import MuscleGroup
from routers.utils.database import engine

router = APIRouter(
    prefix="/muscles",
    tags=["muscles"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Muscle)
def create_muscle(muscle: Muscle):
    with Session(engine) as session:
        session.add(muscle)
        session.commit()
        session.refresh(muscle)
        return muscle


@router.get("/", response_model=list[Muscle])
def get_muscles():
    with Session(engine) as session:
        muscles = session.exec(select(Muscle)).all()
        return muscles
