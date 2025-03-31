from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Form, Request
from sqlmodel import Session, select
from starlette import status
from starlette.responses import RedirectResponse

from models.models import Exercise, Workout, WorkoutExercise
from routers import templates
from shared.utils.database import engine
from shared.utils.order_exercises import increment_exercise_order

router = APIRouter(
    prefix="/html/workouts",
    tags=["html", "workouts"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{workout_id}/update", response_model=Workout)
def update_workout_html(
    workout_id: int,
    date: Annotated[str, Form()],
    duration: Annotated[int, Form()],
):
    with Session(engine) as session:
        workout = session.exec(select(Workout).where(Workout.id == workout_id)).one()
        # workout.template_id = workout.template_id
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        workout.date = date_obj
        workout.duration = duration
        session.add(workout)
        session.commit()
        session.refresh(workout)

        return RedirectResponse(
            router.url_path_for("get_workout_html", workout_id=workout.id),
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.get("/{workout_id}", response_model=Workout)
def get_workout_html(request: Request, workout_id: int):
    with Session(engine) as session:
        workout = session.exec(select(Workout).where(Workout.id == workout_id)).one()
        exercises = session.exec(select(Exercise)).all()

        return templates.TemplateResponse(
            request=request,
            name="workout.html",
            context={"workout": workout, "exercises": exercises},
        )


@router.post("/{workout_id}/workout_exercises/", response_model=WorkoutExercise)
def create_workout_exercise_html(
    workout_id: int,
    order: Annotated[int, Form()],
    exercise_id: Annotated[int, Form()],
    notes: Annotated[str, Form()] = "",
):
    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        order=order,
        exercise_id=exercise_id,
        notes=notes,
    )
    with Session(engine) as session:
        increment_exercise_order(session, WorkoutExercise, workout_id, order)
        session.add(workout_exercise)
        session.commit()
        session.refresh(workout_exercise)

    return RedirectResponse(
        router.url_path_for("get_workout_html", workout_id=workout_id),
        status_code=status.HTTP_303_SEE_OTHER,
    )
