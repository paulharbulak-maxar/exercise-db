from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select

from models.models import Workout, WorkoutExercise
from models.schemas import (
    WorkoutCreate,
    WorkoutExerciseCreate,
    WorkoutExerciseRead,
    WorkoutRead,
    WorkoutUpdate,
)
from shared.utils.database import engine
from shared.utils.order_exercises import increment_exercise_order

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
    responses={404: {"description": "Not found"}},
)


# TODO: Implement using Depends
def get_session():
    with Session(engine) as session:
        yield session


@router.post("", response_model=WorkoutRead)
def create_workout(workout: WorkoutCreate):
    db_workout = Workout(**workout.model_dump())

    with Session(engine) as session:
        session.add(db_workout)
        session.commit()
        session.refresh(db_workout)

    return db_workout


@router.put("/{workout_id}", response_model=WorkoutRead)
def update_workout(workout_id: int, workout: WorkoutUpdate):
    with Session(engine) as session:
        db_workout = session.get(Workout, workout_id)

        if not db_workout:
            raise HTTPException(status_code=404, detail="Workout not found")

        workout_data = workout.model_dump(exclude_unset=True)

        for key, value in workout_data.items():
            if key == "id":
                continue
            setattr(db_workout, key, value)

        session.add(db_workout)
        session.commit()
        session.refresh(db_workout)

    return db_workout


# TODO: Add program name and program type query filters (name)
# Program type -> program -> workouts
@router.get("", response_model=list[WorkoutRead])
def get_workouts(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    with Session(engine) as session:
        workouts = session.exec(select(Workout).offset(offset).limit(limit)).all()

    return workouts


@router.get("/{workout_id}", response_model=WorkoutRead)
def get_workout(workout_id: int):
    with Session(engine) as session:
        workout = session.get(Workout, workout_id)

        if not workout:
            raise HTTPException(status_code=404, detail="Workout not found")

    return workout


@router.delete("/{workout_id}", status_code=204)
def delete_workout(workout_id: int):
    with Session(engine) as session:
        workout = session.get(Workout, workout_id)

        if not workout:
            raise HTTPException(status_code=404, detail="Workout not found")

        session.delete(workout)
        session.commit()


@router.post("/{workout_id}/workout_exercises", response_model=WorkoutExerciseRead)
def create_workout_exercise(workout_id: int, workout_exercise: WorkoutExerciseCreate):
    db_workout_exercise = WorkoutExercise(**workout_exercise.model_dump())

    with Session(engine) as session:
        increment_exercise_order(
            session,
            WorkoutExercise,
            workout_id,
            db_workout_exercise.order,
            foreign_key="workout_id",
        )
        session.add(db_workout_exercise)
        session.commit()
        session.refresh(db_workout_exercise)

    return db_workout_exercise


@router.get("/{workout_id}/exercises", response_model=list[WorkoutExerciseRead])
def get_workout_exercises(workout_id: int = None):
    with Session(engine) as session:
        workout_exercises = session.exec(
            select(WorkoutExercise).where(WorkoutExercise.workout_id == workout_id)
        ).all()

        return workout_exercises
