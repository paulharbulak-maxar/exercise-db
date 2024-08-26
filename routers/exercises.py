from fastapi import APIRouter
from sqlmodel import Session, select

from models.emg_activation import EmgActivation
from models.exercise import Exercise
from models.muscle import Muscle
from routers.utils.database import engine

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Exercise)
def create_exercise(exercise: Exercise):
    with Session(engine) as session:
        session.add(exercise)
        session.commit()
        session.refresh(exercise)
        return exercise


@router.get("/", response_model=list[Exercise])
def get_exercises():
    with Session(engine) as session:
        exercises = session.exec(select(Exercise)).all()
        return exercises
