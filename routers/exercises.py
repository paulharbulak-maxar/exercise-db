from typing import Annotated, Optional

from fastapi import APIRouter, Form
from sqlmodel import Session, select
from starlette import status
from starlette.responses import RedirectResponse

from models.emg_activation import EmgActivation
from models.exercise import Exercise
from models.muscle import Muscle
from routers.programs import router as program_router
from routers.utils.database import engine

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Exercise)
# def create_exercise(exercise: Exercise):
def create_exercise(
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

        # return exercise
        return RedirectResponse(
            program_router.url_path_for("get_programs"),
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.get("/", response_model=list[Exercise])
def get_exercises():
    with Session(engine) as session:
        exercises = session.exec(select(Exercise)).all()

        return exercises
