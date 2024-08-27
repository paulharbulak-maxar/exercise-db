from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Form, Request
from sqlmodel import Session, select
from starlette import status
from starlette.responses import RedirectResponse

from models.program import Program
from models.program_type import ProgramType
from models.template_exercise import TemplateExercise
from models.workout import Workout
from models.workout_template import WorkoutTemplate
from routers import templates
from routers.utils.database import engine
from routers.workout_templates import router as template_router

router = APIRouter(
    prefix="/programs",
    tags=["programs"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Program)
# def create_program(program: Program):
def create_program(
    name: Annotated[str, Form()],
    program_type_id: Annotated[int, Form()],
    start_date: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
):
    program = Program(
        name=name,
        program_type_id=program_type_id,
        start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
        description=description,
    )

    with Session(engine) as session:
        session.add(program)
        session.commit()
        session.refresh(program)

        return RedirectResponse(
            router.url_path_for("get_program", program_id=program.id),
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.get("/", response_model=list[Program])
def get_programs(request: Request):
    with Session(engine) as session:
        programs = session.exec(select(Program)).all()
        program_types = session.exec(select(ProgramType)).all()
        return templates.TemplateResponse(
            request=request,
            name="programs.html",
            context={"programs": programs, "program_types": program_types},
        )

        # return programs


@router.get("/{program_id}", response_model=list[Program])
def get_program(request: Request, program_id: int):
    with Session(engine) as session:
        program = session.exec(select(Program).where(Program.id == program_id)).one()
        workout_templates = session.exec(
            select(WorkoutTemplate).where(WorkoutTemplate.program_id == program_id)
        ).all()

        return templates.TemplateResponse(
            request=request,
            name="selected_program.html",
            context={"program": program, "workout_templates": workout_templates},
        )


# @router.delete("/program_id/{workout_exercise_id}")
@router.post("/{program_id}/delete", response_model=Program)
def delete_program(program_id: int):
    with Session(engine) as session:
        program = session.exec(select(Program).where(Program.id == program_id)).one()

        session.delete(program)
        session.commit()

        return RedirectResponse(
            router.url_path_for("get_programs"),
            status_code=status.HTTP_303_SEE_OTHER,
        )


# Workout Template
# Form for selecting n number of exercises for each workout
@router.post("/{program_id}/workout_templates/", response_model=WorkoutTemplate)
# def create_workout_template(workout_template: WorkoutTemplate):
def create_workout_template(
    program_id: int,
    day_of_week: Annotated[int, Form()],
    label: Annotated[str, Form()],
):
    workout_template = WorkoutTemplate(
        program_id=program_id,
        day_of_week=day_of_week,
        label=label,
    )

    with Session(engine) as session:
        session.add(workout_template)
        session.commit()
        session.refresh(workout_template)

        return RedirectResponse(
            template_router.url_path_for(
                "get_workout_template", template_id=workout_template.id
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )
