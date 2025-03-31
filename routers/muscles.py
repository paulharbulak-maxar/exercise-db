from fastapi import APIRouter
from sqlmodel import Session, select

from models.models import Muscle, MuscleResponse
from shared.utils.database import engine

router = APIRouter(
    prefix="/muscles",
    tags=["muscles"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=MuscleResponse)
def create_muscle(muscle: Muscle):
    with Session(engine) as session:
        session.add(muscle)
        session.commit()
        session.refresh(muscle)
        return muscle


@router.get("/", response_model=list[MuscleResponse])
def get_muscles():
    with Session(engine) as session:
        muscles = session.exec(select(Muscle)).all()
        return muscles
