from datetime import date, datetime
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select

from initialize_db import insert_records
from models.models import (
    Exercise,
    Muscle,
    MuscleGroup,
    Program,
    ProgramType,
    User,
    UserExercise,
    UserSet,
    Workout,
)

sqlite_file_name = "exercise.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
templates = Jinja2Templates(directory="templates/")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    insert_records(engine)


app = FastAPI()


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


# User
@app.post("/users/", response_model=User)
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@app.get("/users/", response_model=list[User])
def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


# Program Type
@app.post("/program_types/", response_model=ProgramType)
def create_program_type(program_type: ProgramType):
    with Session(engine) as session:
        session.add(program_type)
        session.commit()
        session.refresh(program_type)
        return program_type


@app.get("/program_types/", response_model=list[ProgramType])
def read_program_types():
    with Session(engine) as session:
        users = session.exec(select(ProgramType)).all()
        return users


# ***************************************
# TODO: Create templates
# Creating programs, viewing a selected program and adding workout templates, creating
# workouts (selecting exercises, entering sets--weight and reps), viewing all workouts in
# program (e.g. - both calendar and list), viewing and updating selected workouts
# workout = select exercise enter weight, enter reps, click button to add another exercise (JS)
# OR just have 6-8 entries and only use what is actually entered
# ***************************************

# Program
# @app.post("/programs/", response_model=Program)
# def create_program(program: Program):
#     with Session(engine) as session:
#         session.add(program)
#         session.commit()
#         session.refresh(program)
#         return program


@app.post("/programs/", response_model=Program)
# def create_program(program: Program):
def create_program(
    name: Annotated[str, Form()],
    program_type_id: Annotated[int, Form()],
    start_date: Annotated[str, Form()],
    description: Annotated[str, Form()],
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
        return program


@app.get("/programs/", response_model=list[Program])
def read_programs(request: Request):
    with Session(engine) as session:
        programs = session.exec(select(Program)).all()
        program_types = session.exec(select(ProgramType)).all()
        return templates.TemplateResponse(
            request=request,
            name="programs.html",
            context={"programs": programs, "program_types": program_types},
        )

        # return programs


# Program Workout
# Form for selecting n number of exercises for each workout
@app.post("/programs/", response_model=Program)
# def create_program(program: Program):
def create_program(
    name: Annotated[str, Form()],
    program_type_id: Annotated[int, Form()],
    start_date: Annotated[str, Form()],
    description: Annotated[str, Form()],
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
        return program


@app.get("/programs/", response_model=list[Program])
def read_programs(request: Request):
    with Session(engine) as session:
        programs = session.exec(select(Program)).all()
        program_types = session.exec(select(ProgramType)).all()
        return templates.TemplateResponse(
            request=request,
            name="programs.html",
            context={"programs": programs, "program_types": program_types},
        )


# Workout
@app.post("/workouts/", response_model=Workout)
# def create_workout(workout: Workout):
def create_workout(program: Annotated[str, Form()]):
    workout = Workout(program_id=program, date=date.today())
    with Session(engine) as session:
        session.add(workout)
        session.commit()
        session.refresh(workout)

        return workout


@app.get("/workouts/", response_model=list[Workout])
def read_workouts(request: Request):
    with Session(engine) as session:
        workouts = session.exec(select(Workout)).all()
        programs = session.exec(select(Program)).all()

        return templates.TemplateResponse(
            request=request,
            name="workouts.html",
            context={"workouts": workouts, "programs": programs},
        )
        # return workouts


# MuscleGroup
@app.post("/muscle_groups/", response_model=MuscleGroup)
def create_muscle_group(muscle_group: MuscleGroup):
    with Session(engine) as session:
        session.add(muscle_group)
        session.commit()
        session.refresh(muscle_group)
        return muscle_group


@app.get("/muscle_groups/", response_model=list[MuscleGroup])
def read_muscle_groups():
    with Session(engine) as session:
        muscle_groups = session.exec(select(MuscleGroup)).all()
        return muscle_groups


# Muscle
@app.post("/muscles/", response_model=Muscle)
def create_muscle(muscle: Muscle):
    with Session(engine) as session:
        session.add(muscle)
        session.commit()
        session.refresh(muscle)
        return muscle


@app.get("/muscles/", response_model=list[Muscle])
def read_muscles():
    with Session(engine) as session:
        muscles = session.exec(select(Muscle)).all()
        return muscles


# Exercise
@app.post("/exercises/", response_model=Exercise)
def create_exercise(exercise: Exercise):
    with Session(engine) as session:
        session.add(exercise)
        session.commit()
        session.refresh(exercise)
        return exercise


@app.get("/exercises/", response_model=list[Exercise])
def read_exercises():
    with Session(engine) as session:
        exercises = session.exec(select(Exercise)).all()
        return exercises


# UserExercise
@app.post("/user_exercises/", response_model=UserExercise)
def create_user_exercise(user_exercise: UserExercise):
    with Session(engine) as session:
        session.add(user_exercise)
        session.commit()
        session.refresh(user_exercise)
        return user_exercise


@app.get("/user_exercises/", response_model=list[UserExercise])
def read_user_exercises():
    with Session(engine) as session:
        user_exercises = session.exec(select(UserExercise)).all()
        return user_exercises


# UserSet
@app.post("/user_sets/", response_model=UserSet)
def create_user(user_set: UserSet):
    with Session(engine) as session:
        session.add(user_set)
        session.commit()
        session.refresh(user_set)
        return user_set


@app.get("/user_sets/", response_model=list[UserSet])
def read_users():
    with Session(engine) as session:
        user_sets = session.exec(select(UserSet)).all()
        return user_sets


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
