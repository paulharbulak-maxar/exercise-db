from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, or_, select

from models.models import Exercise, ExerciseResponse, Muscle, MuscleGroup
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


@router.get("", response_model=list[ExerciseResponse])
def get_exercises(
    muscle: str = None,
    muscle_group: str = None,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    with Session(engine) as session:
        query = select(Exercise).offset(offset).limit(limit)
        if muscle:
            muscle_result = session.exec(
                select(Muscle).where(Muscle.name == muscle)
            ).first()

            query = query.where(
                or_(
                    Exercise.muscle_primary == muscle_result.id,
                    Exercise.muscle_secondary == muscle_result.id,
                )
            )

        if muscle_group:
            muscle_group_result = session.exec(
                select(MuscleGroup).where(MuscleGroup.name == muscle_group)
            ).first()

            muscles = session.exec(
                select(Muscle).where(Muscle.muscle_group == muscle_group_result)
            ).all()

            muscle_list = [m.id for m in muscles]
            query = query.where(
                or_(
                    Exercise.muscle_primary.in_(muscle_list),
                    Exercise.muscle_secondary.in_(muscle_list),
                )
            )

        exercises = session.exec(query).all()

        return exercises


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int):
    with Session(engine) as session:
        exercise = session.get(Exercise, exercise_id)

        if exercise is None:
            raise HTTPException(status_code=404, detail="Exercise not found")

        return exercise


@router.delete("/{exercise_id}", status_code=204)
def delete_exercise(exercise_id: int):
    with Session(engine) as session:
        exercise = session.get(Exercise, exercise_id)

        if exercise is None:
            raise HTTPException(status_code=404, detail="Exercise not found")

        session.delete(exercise)
        session.commit()
