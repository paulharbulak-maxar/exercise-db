from fastapi import APIRouter
from sqlmodel import Session, select

from models.models import TemplateExercise, TemplateExerciseResponse
from shared.utils.database import engine
from shared.utils.order_exercises import decrement_exercise_order, update_exercise_order

router = APIRouter(
    prefix="/template_exercises",
    tags=["template_exercises"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{template_exercise_id}", response_model=TemplateExerciseResponse)
def create_template_exercise(template_exercise: TemplateExercise):
    with Session(engine) as session:
        session.add(template_exercise)
        session.commit()
        session.refresh(template_exercise)

    return template_exercise


@router.get("/{template_exercise_id}", response_model=TemplateExerciseResponse)
def get_template_exercise(template_exercise_id: int):
    with Session(engine) as session:
        template_exercise = session.exec(
            select(TemplateExercise).where(TemplateExercise.id == template_exercise_id)
        ).one()

    return template_exercise


@router.delete("/{template_exercise_id}", response_model=dict)
def delete_template_exercise(template_exercise_id: int):
    with Session(engine) as session:
        template_exercise = session.exec(
            select(TemplateExercise).where(TemplateExercise.id == template_exercise_id)
        ).one()

        decrement_exercise_order(session, template_exercise, "workout_template_id")
        session.delete(template_exercise)
        session.commit()

        return {"deleted": template_exercise.id}


@router.put("/{template_exercise_id}", response_model=TemplateExerciseResponse)
def update_template_exercise(
    template_exercise_id: int,
    order: int,
):
    with Session(engine) as session:
        template_exercise = session.exec(
            select(TemplateExercise).where(TemplateExercise.id == template_exercise_id)
        ).one()

        if order != template_exercise.order:
            update_exercise_order(
                session, template_exercise, order, "workout_template_id"
            )
            template_exercise.order = order

        session.add(template_exercise)
        session.commit()
        session.refresh(template_exercise)

    return template_exercise
