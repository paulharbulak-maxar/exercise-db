from fastapi import APIRouter
from sqlmodel import Session, select

from models.program import Program
from models.program_type import ProgramType
from routers.utils.database import engine

router = APIRouter(
    prefix="/program_types",
    tags=["program_types"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=ProgramType)
def create_program_type(program_type: ProgramType):
    with Session(engine) as session:
        session.add(program_type)
        session.commit()
        session.refresh(program_type)
        return program_type


@router.get("/", response_model=list[ProgramType])
def get_program_types():
    with Session(engine) as session:
        program_types = session.exec(select(ProgramType)).all()
        return program_types
