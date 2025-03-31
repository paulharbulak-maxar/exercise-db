from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.models import ProgramType, ProgramTypeResponse
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
        program = session.exec(
            select(ProgramType).where(ProgramType.id == program_type_id)
        ).first()

        if program is None:
            raise HTTPException(status_code=404, detail="Program type not found")

        return program


# TODO: Create route for delete
# TODO: Create route for GET programs by program_type
