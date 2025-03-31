from fastapi import APIRouter, Request
from sqlmodel import Session, select

from models.models import (
    Program,
    ProgramResponse,
    WorkoutTemplate,
    WorkoutTemplateResponse,
)
from shared.utils.database import engine

router = APIRouter(
    prefix="/programs",
    tags=["programs"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=ProgramResponse)
def create_program(program: Program):
    with Session(engine) as session:
        session.add(program)
        session.commit()
        session.refresh(program)

    return program


@router.get("/", response_model=list[ProgramResponse])
def get_programs():
    with Session(engine) as session:
        programs = session.exec(select(Program)).all()

    return programs


@router.get("/{program_id}", response_model=ProgramResponse)
def get_program(request: Request, program_id: int):
    with Session(engine) as session:
        program = session.exec(select(Program).where(Program.id == program_id)).one()

    return program


@router.delete("/{program_id}")
def delete_program(program_id: int):
    with Session(engine) as session:
        program = session.exec(select(Program).where(Program.id == program_id)).one()

        session.delete(program)
        session.commit()

    return


# Workout Template
# Form for selecting n number of exercises for each workout
@router.post("/{program_id}/workout_templates/", response_model=WorkoutTemplateResponse)
def create_workout_template(workout_template: WorkoutTemplate):
    with Session(engine) as session:
        session.add(workout_template)
        session.commit()
        session.refresh(workout_template)

    return workout_template
