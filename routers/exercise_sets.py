from fastapi import APIRouter
from sqlmodel import Session, select

from models.models import ExerciseSet, ExerciseSetResponse
from shared.utils.database import engine

router = APIRouter(
    prefix="/exercise_sets",
    tags=["exercise_sets"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{exercise_set_id}", response_model=ExerciseSetResponse)
def get_exercise_set(exercise_set_id: int):
    with Session(engine) as session:
        exercise_sets = session.exec(
            select(ExerciseSet).where(ExerciseSet.id == exercise_set_id)
        ).all()

        return exercise_sets
