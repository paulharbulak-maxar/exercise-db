from fastapi import APIRouter
from sqlmodel import Session, select

from models.template_exercise import TemplateExercise
from models.workout import Workout
from models.workout_exercise import WorkoutExercise
from models.workout_template import WorkoutTemplate
from routers.utils.database import engine

router = APIRouter(
    prefix="/workout_templates",
    tags=["workout_templates"],
    responses={404: {"description": "Not found"}},
)


@router.put("/{template_id}", response_model=WorkoutTemplate)
def update_workout_template(workout_template: WorkoutTemplate):
    with Session(engine) as session:
        session.add(workout_template)
        session.commit()

    return workout_template


@router.get("/{template_id}", response_model=list[WorkoutTemplate])
def get_workout_template(template_id: int):
    with Session(engine) as session:
        workout_template = session.exec(
            select(WorkoutTemplate).where(WorkoutTemplate.id == template_id)
        ).one()

        return workout_template


@router.post(
"/{workout_template_id}/template_exercises/",
    response_model=TemplateExercise,
)
def create_template_exercise(
    workout_template_id: int, template_exercise: TemplateExercise
):
    with Session(engine) as session:
        workout_template = session.exec(
            select(WorkoutTemplate).where(WorkoutTemplate.id == workout_template_id)
        ).one()

        if not template_exercise.order:
            template_exercise.order = len(workout_template.exercises) + 1

        session.add(template_exercise)
        session.commit()

        return template_exercise


# Workout
@router.post("/{template_id}/workouts/", response_model=Workout)
def create_workout(template_id: int, workout: Workout):
    with Session(engine) as session:
        session.add(workout)
        session.commit()
        session.refresh(workout)

        # Automatically create exercises for new workout using template exercises
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

    # TODO: Return list of exercises with workout?
    return workout
