from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.models import (
    TemplateExercise,
    TemplateExerciseResponse,
    Workout,
    WorkoutExercise,
    WorkoutResponse,
    WorkoutTemplate,
    WorkoutTemplateResponse,
)
from shared.utils.database import engine

router = APIRouter(
    prefix="/workout_templates",
    tags=["workout_templates"],
    responses={404: {"description": "Not found"}},
)


@router.put("/{template_id}", response_model=WorkoutTemplateResponse)
def update_workout_template(workout_template: WorkoutTemplate):
    with Session(engine) as session:
        session.add(workout_template)
        session.commit()

    return workout_template


@router.get("/{template_id}", response_model=WorkoutTemplateResponse)
def get_workout_template(template_id: int):
    with Session(engine) as session:
        workout_template = session.get(WorkoutTemplate, template_id)

        if not workout_template:
            raise HTTPException(status_code=404, detail="Workout template not found")

        return workout_template


@router.post(
    "/{workout_template_id}/template_exercises",
    response_model=TemplateExerciseResponse,
)
def create_template_exercise(
    workout_template_id: int, template_exercise: TemplateExercise
):
    with Session(engine) as session:
        workout_template = session.get(WorkoutTemplate, workout_template_id)

        if not template_exercise.order:
            template_exercise.order = len(workout_template.exercises) + 1

        session.add(template_exercise)
        session.commit()

        return template_exercise


# Workout
@router.post("/{template_id}/workouts", response_model=WorkoutResponse)
def create_workout(template_id: int, workout: Workout):
    with Session(engine) as session:
        session.add(workout)
        session.commit()
        session.refresh(workout)

        # Automatically create exercises for new workout using template exercises
        workout_template = session.get(WorkoutTemplate, template_id)

        for template_ex in workout_template.exercises:
            workout_exercise = WorkoutExercise(
                order=template_ex.order,
                workout_id=workout.id,
                exercise_id=template_ex.exercise.id,
            )
            session.add(workout_exercise)

        session.commit()

    return workout


@router.delete("/{template_id}", status_code=204)
def delete_workout_template(template_id: int):
    with Session(engine) as session:
        workout_template = session.get(WorkoutTemplate, template_id)

        if not workout_template:
            raise HTTPException(status_code=404, detail="Workout template not found")

        session.delete(workout_template)
        session.commit()


@router.get("/{template_id}/exercises", response_model=list[TemplateExercise])
def get_workout_template_exercises(template_id: int):
    with Session(engine) as session:
        workout_template = session.get(WorkoutTemplate, template_id)

        if not workout_template:
            raise HTTPException(status_code=404, detail="Workout template not found")

        return workout_template.exercises
