from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select

from initialize_db import insert_records
from models.models import (
    Exercise,
    Muscle,
    MuscleGroup,
    Program,
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


# Program
@app.post("/programs/", response_model=Program)
def create_program(program: Program):
    with Session(engine) as session:
        session.add(program)
        session.commit()
        session.refresh(program)
        return program


@app.get("/programs/", response_model=list[Program])
def read_programs(request: Request):
    with Session(engine) as session:
        programs = session.exec(select(Program)).all()
        return templates.TemplateResponse(
            request=request, name="test.html", context={"programs": programs}
        )

        # return programs


# Workout
@app.post("/workouts/", response_model=Workout)
def create_workout(workout: Workout):
    with Session(engine) as session:
        session.add(workout)
        session.commit()
        session.refresh(workout)
        return workout


@app.get("/workouts/", response_model=list[Workout])
def read_workouts():
    with Session(engine) as session:
        workouts = session.exec(select(Workout)).all()
        return workouts


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
