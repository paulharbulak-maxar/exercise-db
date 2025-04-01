from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.models import ProgramResponse, ProgramType, ProgramTypeResponse
from shared.utils.database import engine

router = APIRouter(
    prefix="/program_types",
    tags=["program_types"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=ProgramTypeResponse)
def create_program_type(program_type: ProgramType):
    with Session(engine) as session:
        session.add(program_type)
        session.commit()
        session.refresh(program_type)
        return program_type


@router.get("", response_model=list[ProgramTypeResponse])
def get_program_types():
    with Session(engine) as session:
        program_types = session.exec(select(ProgramType)).all()
        return program_types


@router.get("/{program_type_id}", response_model=ProgramTypeResponse)
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


@router.get("/{program_type_id}/programs", response_model=list[ProgramResponse])
def get_programs_by_program_type(program_type_id: int):
    with Session(engine) as session:
        program_type = session.get(ProgramType, program_type_id)

        if program_type is None:
            raise HTTPException(status_code=404, detail="Program type not found")

        return program_type.programs
