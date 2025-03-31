from fastapi import APIRouter, HTTPException, Request
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


@router.post("", response_model=ProgramResponse)
def create_program(program: Program):
    with Session(engine) as session:
        session.add(program)
        session.commit()
        session.refresh(program)

    return program


# TODO: Add program type name query filter
@router.get("", response_model=list[ProgramResponse])
def get_programs():
    with Session(engine) as session:
        programs = session.exec(select(Program)).all()

    return programs


@router.get("/{program_id}", response_model=ProgramResponse)
def get_program(program_id: int):
    with Session(engine) as session:
        program = session.get(Program, program_id)

        if not program:
            raise HTTPException(status_code=404, detail="Program not found")

        return program


@router.delete("/{program_id}", status_code=204)
def delete_program(program_id: int):
    with Session(engine) as session:
        program = session.get(Program, program_id)
        session.delete(program)
        session.commit()


# Workout Template
@router.post("/{program_id}/workout_templates", response_model=WorkoutTemplateResponse)
def create_workout_template(workout_template: WorkoutTemplate):
    with Session(engine) as session:
        session.add(workout_template)
        session.commit()
        session.refresh(workout_template)

    return workout_template


# TODO: Create route for GET and PUT workout_templates
