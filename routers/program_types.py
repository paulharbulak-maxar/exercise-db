from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.models import ProgramType
from models.schemas import ProgramRead, ProgramTypeCreate, ProgramTypeRead
from shared.utils.database import engine

router = APIRouter(
    prefix="/program_types",
    tags=["program_types"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=ProgramTypeRead)
def create_program_type(program_type: ProgramTypeCreate):
    db_program_type = ProgramType(**program_type.model_dump())

    with Session(engine) as session:
        session.add(db_program_type)
        session.commit()
        session.refresh(db_program_type)
        return db_program_type


@router.get("", response_model=list[ProgramTypeRead])
def get_program_types():
    with Session(engine) as session:
        program_types = session.exec(select(ProgramType)).all()
        return program_types


# TODO: Create context manager for getting program_type by id and checking if None
@router.get("/{program_type_id}", response_model=ProgramTypeRead)
def get_program_type(program_type_id: int):
    with Session(engine) as session:
        program_type = session.get(ProgramType, program_type_id)

        if program_type is None:
            raise HTTPException(status_code=404, detail="Program type not found")

        return program_type


@router.delete("/{program_type_id}", status_code=204)
def delete_program_type(program_type_id: int):
    with Session(engine) as session:
        program_type = session.get(ProgramType, program_type_id)

        if program_type is None:
            raise HTTPException(status_code=404, detail="Program type not found")

        session.delete(program_type)
        session.commit()


@router.get("/{program_type_id}/programs", response_model=list[ProgramRead])
def get_programs_by_program_type(program_type_id: int):
    with Session(engine) as session:
        program_type = session.get(ProgramType, program_type_id)

        if program_type is None:
            raise HTTPException(status_code=404, detail="Program type not found")

        return program_type.programs
