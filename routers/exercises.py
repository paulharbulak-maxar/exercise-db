from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select

from models.models import Exercise, ExerciseResponse
from shared.utils.database import engine

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=ExerciseResponse)
def create_exercise(exercise: Exercise):
    with Session(engine) as session:
        session.add(exercise)
        session.commit()
        session.refresh(exercise)

        return exercise


# TODO: Add muscle and muscle group name query filters
@router.get("", response_model=list[ExerciseResponse])
def get_exercises(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    with Session(engine) as session:
        exercises = session.exec(select(Exercise).offset(offset).limit(limit)).all()

        return exercises


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int):
    with Session(engine) as session:
        exercise = session.exec(
            select(Exercise).where(Exercise.id == exercise_id)
        ).first()

        if exercise is None:
            raise HTTPException(status_code=404, detail="Exercise not found")

        return exercise


# TODO: Create route for delete
