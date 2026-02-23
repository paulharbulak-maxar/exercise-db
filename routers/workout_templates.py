from fastapi import APIRouter, HTTPException
from sqlmodel import Session

from models.models import TemplateExercise, Workout, WorkoutExercise, WorkoutTemplate
from models.schemas import (
    TemplateExerciseCreate,
    TemplateExerciseRead,
    WorkoutCreate,
    WorkoutRead,
    WorkoutTemplateRead,
    WorkoutTemplateUpdate,
)
from shared.utils.database import engine

router = APIRouter(
    prefix="/workout_templates",
    tags=["workout_templates"],
    responses={404: {"description": "Not found"}},
)


@router.put("/{template_id}", response_model=WorkoutTemplateRead)
def update_workout_template(
    template_id: int,
    workout_template: WorkoutTemplateUpdate,
):
    with Session(engine) as session:
        db_template = session.get(WorkoutTemplate, template_id)

        if not db_template:
            raise HTTPException(status_code=404, detail="Workout template not found")

        template_data = workout_template.model_dump(exclude_unset=True)

        for key, value in template_data.items():
            if key == "id":
                continue
            setattr(db_template, key, value)

        session.add(db_template)
        session.commit()
        session.refresh(db_template)

    return db_template


@router.get("/{template_id}", response_model=WorkoutTemplateRead)
def get_workout_template(template_id: int):
    with Session(engine) as session:
        workout_template = session.get(WorkoutTemplate, template_id)

        if not workout_template:
            raise HTTPException(status_code=404, detail="Workout template not found")

        return workout_template


@router.post(
    "/{workout_template_id}/template_exercises",
    response_model=TemplateExerciseRead,
)
def create_template_exercise(
    workout_template_id: int, template_exercise: TemplateExerciseCreate
):
    with Session(engine) as session:
        workout_template = session.get(WorkoutTemplate, workout_template_id)

        if not workout_template:
            raise HTTPException(status_code=404, detail="Workout template not found")

        db_template_exercise = TemplateExercise(**template_exercise.model_dump())
        db_template_exercise.workout_template_id = workout_template_id

        if not db_template_exercise.order:
            db_template_exercise.order = len(workout_template.exercises) + 1

        session.add(db_template_exercise)
        session.commit()
        session.refresh(db_template_exercise)

        return db_template_exercise


# Workout
@router.post("/{template_id}/workouts", response_model=WorkoutRead)
def create_workout(template_id: int, workout: WorkoutCreate):
    db_workout = Workout(**workout.model_dump())

    with Session(engine) as session:
        workout_template = session.get(WorkoutTemplate, template_id)

        if not workout_template:
            raise HTTPException(status_code=404, detail="Workout template not found")

        session.add(db_workout)
        session.commit()
        session.refresh(db_workout)

        # Automatically create exercises for new workout using template exercises
        for template_ex in workout_template.exercises:
            workout_exercise = WorkoutExercise(
                order=template_ex.order,
                workout_id=db_workout.id,
                exercise_id=template_ex.exercise_id,
            )
            session.add(workout_exercise)

        session.commit()
        session.refresh(db_workout)

    return db_workout


@router.delete("/{template_id}", status_code=204)
def delete_workout_template(template_id: int):
    with Session(engine) as session:
        workout_template = session.get(WorkoutTemplate, template_id)

        if not workout_template:
            raise HTTPException(status_code=404, detail="Workout template not found")

        session.delete(workout_template)
        session.commit()


@router.get("/{template_id}/exercises", response_model=list[TemplateExerciseRead])
def get_workout_template_exercises(template_id: int):
    with Session(engine) as session:
        workout_template = session.get(WorkoutTemplate, template_id)

        if not workout_template:
            raise HTTPException(status_code=404, detail="Workout template not found")

        return workout_template.exercises
