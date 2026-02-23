from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.models import ExerciseSet, WorkoutExercise
from models.schemas import (
    ExerciseSetCreate,
    ExerciseSetRead,
    WorkoutExerciseRead,
    WorkoutExerciseUpdate,
)
from shared.utils.database import engine
from shared.utils.order_exercises import decrement_exercise_order, update_exercise_order

router = APIRouter(
    prefix="/workout_exercises",
    tags=["workout_exercises"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{workout_exercise_id}", response_model=WorkoutExerciseRead)
def get_workout_exercise(workout_exercise_id: int):
    with Session(engine) as session:
        workout_exercise = session.exec(
            select(WorkoutExercise).where(WorkoutExercise.id == workout_exercise_id)
        ).first()

        if workout_exercise is None:
            raise HTTPException(status_code=404, detail="Workout exercise not found")

        return workout_exercise


@router.put("/{workout_exercise_id}", response_model=WorkoutExerciseRead)
def update_workout_exercise(
    workout_exercise_id: int, workout_exercise: WorkoutExerciseUpdate
):
    with Session(engine) as session:
        db_workout_exercise = session.get(WorkoutExercise, workout_exercise_id)

        if not db_workout_exercise:
            raise HTTPException(status_code=404, detail="Workout exercise not found")

        if workout_exercise.order != db_workout_exercise.order:
            update_exercise_order(
                session,
                db_workout_exercise,
                workout_exercise.order,
                foreign_key="workout_id",
            )
            db_workout_exercise.order = workout_exercise.order

        workout_exercise_data = workout_exercise.model_dump(exclude_unset=True)
        for key, value in workout_exercise_data.items():
            setattr(db_workout_exercise, key, value)

        session.add(db_workout_exercise)
        session.commit()
        session.refresh(db_workout_exercise)

        return db_workout_exercise


@router.delete("/{workout_exercise_id}", status_code=204)
def delete_workout_exercise(workout_exercise_id: int):
    with Session(engine) as session:
        workout_exercise = session.exec(
            select(WorkoutExercise).where(WorkoutExercise.id == workout_exercise_id)
        ).first()

        if workout_exercise is None:
            raise HTTPException(status_code=404, detail="Workout exercise not found")

        decrement_exercise_order(session, workout_exercise, "workout_id")
        session.delete(workout_exercise)
        session.commit()


@router.post("/{workout_exercise_id}/exercise_sets", response_model=ExerciseSetRead)
def create_exercise_set(workout_exercise_id: int, exercise_set: ExerciseSetCreate):
    with Session(engine) as session:
        workout_exercise = session.get(WorkoutExercise, workout_exercise_id)

        if workout_exercise is None:
            raise HTTPException(status_code=404, detail="Workout exercise not found")

        db_exercise_set = ExerciseSet(**exercise_set.model_dump())
        db_exercise_set.workout_exercise_id = workout_exercise_id
        session.add(db_exercise_set)
        session.commit()
        session.refresh(db_exercise_set)

        return db_exercise_set


@router.get(
    "/{workout_exercise_id}/exercise_sets", response_model=list[ExerciseSetRead]
)
def get_exercise_sets(workout_exercise_id: int):
    with Session(engine) as session:
        workout_exercise = session.get(WorkoutExercise, workout_exercise_id)

        if workout_exercise is None:
            raise HTTPException(status_code=404, detail="Workout exercise not found")

        exercise_sets = session.exec(
            select(ExerciseSet).where(
                ExerciseSet.workout_exercise_id == workout_exercise_id
            )
        ).all()

        return exercise_sets
