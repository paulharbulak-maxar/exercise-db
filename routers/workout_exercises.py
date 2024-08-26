from typing import Annotated

from fastapi import APIRouter, Form, Request
from sqlmodel import Session, select
from starlette import status
from starlette.responses import RedirectResponse

from models.exercise import Exercise
from models.exercise_set import ExerciseSet
from models.workout import Workout
from models.workout_exercise import WorkoutExercise
from routers import templates
from routers.utils.database import engine
from routers.utils.order_exercises import (
    decrement_exercise_order,
    update_exercise_order,
)
from routers.workouts import router as workout_router

router = APIRouter(
    prefix="/workout_exercises",
    tags=["workout_exercises"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{workout_exercise_id}", response_model=WorkoutExercise)
# def get_workout_exercise(workout_exercise_id: int):
def get_workout_exercise(request: Request, workout_exercise_id: int):
    with Session(engine) as session:
        workout_exercise = session.exec(
            select(WorkoutExercise).where(WorkoutExercise.id == workout_exercise_id)
        ).one()

        exercises = session.exec(select(Exercise)).all()

        return templates.TemplateResponse(
            request=request,
            name="workout_exercise.html",
            context={"workout_exercise": workout_exercise, "exercises": exercises},
        )


# @router.put("/workout_exercises/{workout_exercise_id}", response_model=WorkoutExercise)
@router.post("/{workout_exercise_id}/update", response_model=WorkoutExercise)
def update_workout_exercise(
    workout_exercise_id: int,
    order: Annotated[int, Form()],
    exercise_id: Annotated[int, Form()],
    notes: Annotated[str, Form()] = "",
):
    with Session(engine) as session:
        workout_exercise = session.exec(
            select(WorkoutExercise).where(WorkoutExercise.id == workout_exercise_id)
        ).one()

        if order != workout_exercise.order:
            update_exercise_order(session, workout_exercise, order)
            workout_exercise.order = order

        workout_exercise.exercise_id = exercise_id
        workout_exercise.notes = notes
        session.add(workout_exercise)
        session.commit()
        session.refresh(workout_exercise)

        # return workout_exercise
        return RedirectResponse(
            workout_router.url_path_for(
                "get_workout", workout_id=workout_exercise.workout_id
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )


# @router.delete("/workout_exercises/{workout_exercise_id}")
@router.post("/{workout_exercise_id}/delete", response_model=WorkoutExercise)
def delete_workout_exercise(workout_exercise_id: int):
    with Session(engine) as session:
        workout_exercise = session.exec(
            select(WorkoutExercise).where(WorkoutExercise.id == workout_exercise_id)
        ).first()

        decrement_exercise_order(session, workout_exercise, "workout_id")
        workout_id = workout_exercise.workout_id
        session.delete(workout_exercise)
        session.commit()

        return RedirectResponse(
            workout_router.url_path_for(
                "get_workout",
                workout_id=workout_id,
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )


# WorkoutSet
@router.post(
    "/{workout_exercise_id}/exercise_sets/",
    response_model=ExerciseSet,
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
    "/workout_exercises/{workout_exercise_id}/exercise_sets/",
    response_model=list[ExerciseSet],
)
def get_exercise_sets(workout_exercise_id: int):
    with Session(engine) as session:
        exercise_sets = session.exec(
            select(ExerciseSet).where(
                ExerciseSet.workout_exercise_id == workout_exercise_id
            )
        ).all()

        return exercise_sets
