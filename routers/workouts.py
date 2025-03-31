from fastapi import APIRouter
from sqlmodel import Session, select

from models.models import (
    Workout,
    WorkoutExercise,
    WorkoutExerciseResponse,
    WorkoutResponse,
)
from shared.utils.database import engine
from shared.utils.order_exercises import increment_exercise_order

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=WorkoutResponse)
def create_workout(workout: Workout):
    with Session(engine) as session:
        session.add(workout)
        session.commit()
        session.refresh(workout)

    return workout


@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_workout(workout: Workout):
    with Session(engine) as session:
        session.add(workout)
        session.commit()

    return workout


@router.get("/", response_model=list[WorkoutResponse])
def get_workouts():
    with Session(engine) as session:
        workouts = session.exec(select(Workout)).all()

    return workouts


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(workout_id: int):
    with Session(engine) as session:
        workout = session.exec(select(Workout).where(Workout.id == workout_id)).one()

    return workout


@router.post("/{workout_id}/workout_exercises/", response_model=WorkoutExerciseResponse)
def create_workout_exercise(workout_id: int, workout_exercise: WorkoutExercise):
    with Session(engine) as session:
        increment_exercise_order(
            session, WorkoutExercise, workout_id, workout_exercise.order
        )
        session.add(workout_exercise)
        session.commit()
        session.refresh(workout_exercise)

    return workout_exercise


@router.get(
    "/{workout_id}/workout_exercises/", response_model=list[WorkoutExerciseResponse]
)
def get_workout_exercises(workout_id: int = None):
    with Session(engine) as session:
        workout_exercises = session.exec(
            select(WorkoutExercise).where(WorkoutExercise.workout_id == workout_id)
        ).all()

        return workout_exercises
