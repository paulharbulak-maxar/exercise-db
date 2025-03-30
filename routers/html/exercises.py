from typing import Annotated, Optional

from fastapi import APIRouter, Form
from sqlmodel import Session
from starlette import status
from starlette.responses import RedirectResponse

from models.exercise import Exercise
from routers.html.programs import router as program_router
from shared.utils.database import engine

router = APIRouter(
    prefix="/html/exercises",
    tags=["html", "exercises"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def create_exercise_html(
    name: Annotated[str, Form()],
    muscle_primary: Annotated[int, Form()],
    muscle_secondary: Optional[int] = Form(None),
    is_compound: Optional[bool] = Form(False),
):
    exercise = Exercise(
        name=name,
        muscle_primary=muscle_primary,
        muscle_secondary=muscle_secondary,
        is_compound=is_compound,
    )

    with Session(engine) as session:
        session.add(exercise)
        session.commit()
        session.refresh(exercise)

        return RedirectResponse(
            program_router.url_path_for("get_programs_html"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
