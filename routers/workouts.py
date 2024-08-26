from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Form, Request
from sqlmodel import Session, select
from starlette import status
from starlette.responses import RedirectResponse

from models.emg_activation import EmgActivation
from models.exercise import Exercise
from models.muscle import Muscle
from models.program import Program
from models.program_type import ProgramType
from models.workout import Workout
from models.workout_exercise import WorkoutExercise
from models.workout_template import WorkoutTemplate
from routers import templates
from routers.utils.database import engine
from routers.utils.order_exercises import increment_exercise_order

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
    responses={404: {"description": "Not found"}},
)


# @router.post("/", response_model=Workout)
# def create_workout(workout: Workout):
#     workout = Workout(template_id=template_id, date=date.today())
#     with Session(engine) as session:
#         session.add(workout)
#         session.commit()
#         session.refresh(workout)
#
#         return workout


# @router.put("/{workout_id}", response_model=Workout)
@router.post("/{workout_id}/update", response_model=Workout)
# def update_workout(date: str, workout_id: int):
def update_workout(
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

        # return workout
        return RedirectResponse(
            router.url_path_for("get_workout", workout_id=workout.id),
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.get("/", response_model=list[Workout])
def get_workouts(request: Request):
    with Session(engine) as session:
        workouts = session.exec(select(Workout)).all()
        programs = session.exec(select(Program)).all()

        return workouts


@router.get("/{workout_id}", response_model=Workout)
def get_workout(request: Request, workout_id: int):
    with Session(engine) as session:
        workout = session.exec(select(Workout).where(Workout.id == workout_id)).one()
        exercises = session.exec(select(Exercise)).all()

        # return workout
        return templates.TemplateResponse(
            request=request,
            name="workout.html",
            context={"workout": workout, "exercises": exercises},
        )


@router.post("/{workout_id}/workout_exercises/", response_model=WorkoutExercise)
def create_workout_exercise(
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
        router.url_path_for("get_workout", workout_id=workout_id),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/{workout_id}/workout_exercises/", response_model=list[WorkoutExercise])
def get_workout_exercises(workout_id: int = None):
    with Session(engine) as session:
        workout_exercises = session.exec(
            select(WorkoutExercise).where(WorkoutExercise.workout_id == workout_id)
        ).all()

        return workout_exercises
