from typing import Annotated

from fastapi import APIRouter, Form, HTTPException
from sqlmodel import Session, select
from starlette import status
from starlette.responses import RedirectResponse

from models.models import (
    ExerciseSet,
    ExerciseSetResponse,
    WorkoutExercise,
    WorkoutExerciseResponse,
)
from routers.html.workouts import router as workout_router
from shared.utils.database import engine
from shared.utils.order_exercises import decrement_exercise_order, update_exercise_order

router = APIRouter(
    prefix="/html/workout_exercises",
    tags=["workout_exercises"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{workout_exercise_id}", response_model=WorkoutExerciseResponse)
def get_workout_exercise(workout_exercise_id: int):
    with Session(engine) as session:
        workout_exercise = session.exec(
            select(WorkoutExercise).where(WorkoutExercise.id == workout_exercise_id)
        ).first()

        if workout_exercise is None:
            raise HTTPException(status_code=404, detail="Workout exercise not found")

        return workout_exercise


# TODO: Test to make sure the logic works with this request
@router.put("/{workout_exercise_id}", response_model=WorkoutExerciseResponse)
def update_workout_exercise(
    workout_exercise_id: int, workout_exercise: WorkoutExercise
):
    with Session(engine) as session:
        db_workout_exercise = session.get(WorkoutExercise, workout_exercise_id)

        if not db_workout_exercise:
            raise HTTPException(status_code=404, detail="Workout exercise not found")

        if workout_exercise.order != db_workout_exercise.order:
            update_exercise_order(session, db_workout_exercise, workout_exercise.order)
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
        ).one()

        decrement_exercise_order(session, workout_exercise, "workout_id")
        workout_id = workout_exercise.workout_id
        session.delete(workout_exercise)
        session.commit()


# WorkoutSet
@router.post(
    "/{workout_exercise_id}/exercise_sets",
    response_model=ExerciseSetResponse,
)
def create_exercise_set(
    workout_exercise_id: int,
    set_number: Annotated[int, Form()],
    weight: Annotated[int, Form()],
    reps: Annotated[int, Form()],
):
    exercise_set = ExerciseSet(
        workout_exercise_id=workout_exercise_id,
        set_number=set_number,
        weight=weight,
        reps=reps,
    )
    with Session(engine) as session:
        session.add(exercise_set)
        session.commit()
        session.refresh(exercise_set)

    return RedirectResponse(
        router.url_path_for(
            "get_workout_exercise", workout_exercise_id=workout_exercise_id
        ),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "/workout_exercises/{workout_exercise_id}/exercise_sets",
    response_model=list[ExerciseSetResponse],
)
def get_exercise_sets(workout_exercise_id: int):
    with Session(engine) as session:
        exercise_sets = session.exec(
            select(ExerciseSet).where(
                ExerciseSet.workout_exercise_id == workout_exercise_id
            )
        ).all()

        return exercise_sets
