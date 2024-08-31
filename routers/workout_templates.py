from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Form, Request
from sqlmodel import Session, select
from starlette import status
from starlette.responses import RedirectResponse

from models.exercise import Exercise
from models.exercise_set import ExerciseSet
from models.muscle import Muscle
from models.muscle_group import MuscleGroup
from models.program import Program
from models.template_exercise import TemplateExercise
from models.workout import Workout
from models.workout_exercise import WorkoutExercise
from models.workout_template import WorkoutTemplate
from routers import templates
from routers.utils.database import engine
from routers.workouts import router as workout_router

router = APIRouter(
    prefix="/workout_templates",
    tags=["workout_templates"],
    responses={404: {"description": "Not found"}},
)


# TODO: Allow updating exercise order in put method
# @router.put("/workout_templates/{template_id}", response_model=WorkoutTemplate)
@router.post("/{template_id}/update", response_model=WorkoutTemplate)
def update_workout_template(
    template_id: int,
    day_of_week: Annotated[int, Form()],
    label: Annotated[str, Form()],
):
    with Session(engine) as session:
        workout_template = session.exec(
            select(WorkoutTemplate).where(WorkoutTemplate.id == template_id)
        ).one()

        workout_template.day_of_week = day_of_week
        workout_template.label = label
        session.add(workout_template)
        session.commit()
        session.refresh(workout_template)

        return RedirectResponse(
            router.url_path_for(
                "get_workout_template", template_id=workout_template.id
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.get("/{template_id}", response_model=list[WorkoutTemplate])
def get_workout_template(request: Request, template_id: int):
    with Session(engine) as session:
        workout_template = session.exec(
            select(WorkoutTemplate).where(WorkoutTemplate.id == template_id)
        ).one()

        muscle_groups = session.exec(select(MuscleGroup)).all()
        muscles = session.exec(select(Muscle)).all()
        exercises = session.exec(select(Exercise)).all()
        return templates.TemplateResponse(
            request=request,
            name="workout_template.html",
            context={
                "workout_template": workout_template,
                "exercises": exercises,
                "muscles": muscles,
                "muscle_groups": muscle_groups,
            },
        )


# TODO: Add workout_template_id to path
@router.post(
    "/{workout_template_id}/template_exercises/",
    response_model=TemplateExercise,
)
def create_template_exercise(
    workout_template_id: int,
    exercise_id: Annotated[int, Form()],
):
    with Session(engine) as session:
        workout_template = session.exec(
            select(WorkoutTemplate).where(WorkoutTemplate.id == workout_template_id)
        ).one()

        template_exercise = TemplateExercise(
            order=len(workout_template.exercises) + 1,
            workout_template_id=workout_template_id,
            exercise_id=exercise_id,
        )

        session.add(template_exercise)
        session.commit()
        session.refresh(template_exercise)

        return RedirectResponse(
            router.url_path_for(
                "get_workout_template",
                template_id=template_exercise.workout_template_id,
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )


# Workout
@router.post("/{template_id}/workouts/", response_model=Workout)
def create_workout(
    template_id: int,
    program_id: Annotated[str, Form()],
):
    workout = Workout(program_id=program_id, template_id=template_id, date=date.today())
    with Session(engine) as session:
        session.add(workout)
        session.commit()
        session.refresh(workout)

        workout_template = session.exec(
            select(WorkoutTemplate).where(WorkoutTemplate.id == template_id)
        ).one()

        for template_ex in workout_template.exercises:
            workout_exercise = WorkoutExercise(
                order=template_ex.order,
                workout_id=workout.id,
                exercise_id=template_ex.exercise.id,
            )
            session.add(workout_exercise)

        session.commit()

        return RedirectResponse(
            workout_router.url_path_for("get_workout", workout_id=workout.id),
            status_code=status.HTTP_303_SEE_OTHER,
        )
