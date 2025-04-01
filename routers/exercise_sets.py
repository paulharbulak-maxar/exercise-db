from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.models import ExerciseSet, ExerciseSetResponse
from shared.utils.database import engine

router = APIRouter(
    prefix="/exercise_sets",
    tags=["exercise_sets"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=ExerciseSetResponse)
def get_exercise_set(exercise_set_id: int):
    with Session(engine) as session:
        exercise_set = session.exec(
            select(ExerciseSet).where(ExerciseSet.id == exercise_set_id)
        ).first()

        if exercise_set is None:
            raise HTTPException(status_code=404, detail="Exercise set not found")

        return exercise_set


@router.post("/{exercise_set_id}", response_model=list[ExerciseSetResponse])
def get_exercise_set(exercise_set_id: int):
    with Session(engine) as session:
        exercise_sets = session.exec(
            select(ExerciseSet).where(ExerciseSet.id == exercise_set_id)
        ).all()

        return exercise_sets


@router.delete("/{exercise_set_id}", status_code=204)
def delete_exercise_set(exercise_set_id: int):
    with Session(engine) as session:
        exercise_set = session.get(ExerciseSet, exercise_set_id)

        if not exercise_set:
            raise HTTPException(status_code=404, detail="Exercise set not found")

        session.delete(exercise_set)
        session.commit()
