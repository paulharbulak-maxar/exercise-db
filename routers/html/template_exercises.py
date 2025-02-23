from fastapi import APIRouter
from sqlmodel import Session, select
from starlette import status
from starlette.responses import RedirectResponse

from models.exercise import Exercise
from models.template_exercise import TemplateExercise
from routers.utils.database import engine
from routers.utils.order_exercises import (
    decrement_exercise_order,
    update_exercise_order,
)
from routers.html.workout_templates import router as template_router

router = APIRouter(
    prefix="/html/template_exercises",
    tags=["template_exercises"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{template_exercise_id}/delete")
def delete_template_exercise_html(template_exercise_id: int):
    with Session(engine) as session:
        template_exercise = session.exec(
            select(TemplateExercise).where(TemplateExercise.id == template_exercise_id)
        ).one()

        decrement_exercise_order(session, template_exercise, "workout_template_id")
        template_id = template_exercise.workout_template_id
        session.delete(template_exercise)
        session.commit()

        return RedirectResponse(
            template_router.url_path_for(
                "get_workout_template_html",
                template_id=template_id,
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.post("/{template_exercise_id}/update", response_model=TemplateExercise)
def update_template_exercise_html(
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

        return RedirectResponse(
            template_router.url_path_for(
                "get_workout_template_html",
                template_id=template_exercise.workout_template_id,
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )
