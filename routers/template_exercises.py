from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.models import TemplateExercise
from models.schemas import TemplateExerciseCreate, TemplateExerciseRead
from shared.utils.database import engine
from shared.utils.order_exercises import decrement_exercise_order, update_exercise_order

router = APIRouter(
    prefix="/template_exercises",
    tags=["template_exercises"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=TemplateExerciseRead)
def create_template_exercise(template_exercise: TemplateExerciseCreate):
    db_template_exercise = TemplateExercise(**template_exercise.model_dump())

    with Session(engine) as session:
        session.add(db_template_exercise)
        session.commit()
        session.refresh(db_template_exercise)

    return db_template_exercise


@router.get("/{template_exercise_id}", response_model=TemplateExerciseRead)
def get_template_exercise(template_exercise_id: int):
    with Session(engine) as session:
        template_exercise = session.exec(
            select(TemplateExercise).where(TemplateExercise.id == template_exercise_id)
        ).first()

    if template_exercise is None:
        raise HTTPException(status_code=404, detail="Template exercise not found")

    return template_exercise


@router.delete("/{template_exercise_id}", status_code=204)
def delete_template_exercise(template_exercise_id: int):
    with Session(engine) as session:
        template_exercise = session.exec(
            select(TemplateExercise).where(TemplateExercise.id == template_exercise_id)
        ).one()

        decrement_exercise_order(session, template_exercise, "workout_template_id")
        session.delete(template_exercise)
        session.commit()


@router.put("/{template_exercise_id}", response_model=TemplateExerciseRead)
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
