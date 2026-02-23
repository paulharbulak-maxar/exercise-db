from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.models import Program, WorkoutTemplate
from models.schemas import (
    ProgramCreate,
    ProgramRead,
    WorkoutRead,
    WorkoutTemplateCreate,
    WorkoutTemplateRead,
)
from shared.utils.database import engine

router = APIRouter(
    prefix="/programs",
    tags=["programs"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=ProgramRead)
def create_program(program: ProgramCreate):
    db_program = Program(**program.model_dump())

    with Session(engine) as session:
        session.add(db_program)
        session.commit()
        session.refresh(db_program)

    return db_program


# TODO: Add program type name query filter
@router.get("", response_model=list[ProgramRead])
def get_programs():
    with Session(engine) as session:
        programs = session.exec(select(Program)).all()

    return programs


@router.get("/{program_id}", response_model=ProgramRead)
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
@router.post("/{program_id}/templates", response_model=WorkoutTemplateRead)
def create_workout_template(program_id: int, workout_template: WorkoutTemplateCreate):
    db_template = WorkoutTemplate(**workout_template.model_dump())
    db_template.program_id = program_id

    with Session(engine) as session:
        program = session.get(Program, program_id)

        if not program:
            raise HTTPException(status_code=404, detail="Program not found")

        session.add(db_template)
        session.commit()
        session.refresh(db_template)

    return db_template


# TODO: Create route for PUT workout_templates
@router.get("/{program_id}/templates", response_model=list[WorkoutTemplateRead])
def get_program_workout_templates(program_id: int):
    with Session(engine) as session:
        program = session.get(Program, program_id)

        if not program:
            raise HTTPException(status_code=404, detail="Program not found")

        return program.workout_templates


@router.get("/{program_id}/workouts", response_model=list[WorkoutRead])
def get_program_workouts(program_id: int):
    with Session(engine) as session:
        program = session.get(Program, program_id)

        if not program:
            raise HTTPException(status_code=404, detail="Program not found")

        return program.workouts
