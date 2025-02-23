from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Form, Request
from sqlmodel import Session, select
from starlette import status
from starlette.responses import RedirectResponse

from models import workout_template
from models.muscle import Muscle
from models.program import Program
from models.program_type import ProgramType
from models.template_exercise import TemplateExercise
from models.workout import Workout
from models.workout_template import WorkoutTemplate
from routers import templates
from routers.html.workout_templates import router as template_router
from routers.utils.database import engine

router = APIRouter(
    prefix="/programs",
    tags=["programs"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Program)
def create_program(program: Program):
    # program = Program(
    #     name=name,
    #     program_type_id=program_type_id,
    #     start_date=datetime.strptime(start_date, "%Y-%m-%d"),
    #     description=description,
    # )

    with Session(engine) as session:
        session.add(program)
        session.commit()
        session.refresh(program)

    return program


@router.get("/", response_model=list[Program])
def get_programs():
    with Session(engine) as session:
        programs = session.exec(select(Program)).all()

    return programs


@router.get("/{program_id}", response_model=list[Program])
def get_program(request: Request, program_id: int):
    with Session(engine) as session:
        program = session.exec(select(Program).where(Program.id == program_id)).one()

    return program


@router.delete("/program_id/{workout_exercise_id}")
def delete_program(program_id: int):
    with Session(engine) as session:
        program = session.exec(select(Program).where(Program.id == program_id)).one()

        session.delete(program)
        session.commit()

    return


# Workout Template
# Form for selecting n number of exercises for each workout
@router.post("/{program_id}/workout_templates/", response_model=WorkoutTemplate)
def create_workout_template(workout_template: WorkoutTemplate):
    # workout_template = WorkoutTemplate(
    #     program_id=program_id,
    #     day_of_week=day_of_week,
    #     label=label,
    # )

    with Session(engine) as session:
        session.add(workout_template)
        session.commit()
        session.refresh(workout_template)

    return workout_template
