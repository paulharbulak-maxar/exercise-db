from datetime import date, datetime
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select
from starlette import status
from starlette.responses import RedirectResponse

from initialize_db import insert_records
from models.models import (
    Exercise,
    Muscle,
    MuscleGroup,
    Program,
    ProgramType,
    TemplateExercise,
    User,
    Workout,
    WorkoutExercise,
    WorkoutSet,
    WorkoutTemplate,
)

sqlite_file_name = "exercise.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
templates = Jinja2Templates(directory="templates/")

DAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]


def get_weekday(d):
    if d > 0 and d <= 7:
        return DAYS[d - 1]
    else:
        return "ERROR"


templates.env.globals["get_weekday"] = get_weekday


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
def get_users():
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
def get_program_types():
    with Session(engine) as session:
        program_types = session.exec(select(ProgramType)).all()
        return program_types


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

        return RedirectResponse(
            app.url_path_for("get_program", program_id=program.id),
            status_code=status.HTTP_303_SEE_OTHER,
        )


@app.get("/programs/", response_model=list[Program])
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


@app.get("/programs/{program_id}", response_model=list[Program])
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


# Workout Template
# Form for selecting n number of exercises for each workout
@app.post("/workout_templates/", response_model=WorkoutTemplate)
# def create_workout_template(workout_template: WorkoutTemplate):
def create_workout_template(
    program_id: Annotated[int, Form()],
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
            app.url_path_for("get_workout_template", template_id=workout_template.id),
            status_code=status.HTTP_303_SEE_OTHER,
        )


# TODO: Allow updating exercise order in put method
@app.put("/workout_templates/{template_id}", response_model=WorkoutTemplate)
def update_workout_template(
    template_id: int,
    program_id: Annotated[int, Form()],
    day_of_week: Annotated[int, Form()],
    label: Annotated[str, Form()],
):
    with Session(engine) as session:
        workout_template = session.exec(
            select(WorkoutTemplate).where(WorkoutTemplate.id == template_id)
        ).one()

        workout_template.program_id = program_id
        workout_template.day_of_week = day_of_week
        workout_template.label = label
        session.add(workout_template)
        session.commit()
        session.refresh(workout_template)

        return RedirectResponse(
            app.url_path_for("get_workout_template", template_id=workout_template.id),
            status_code=status.HTTP_303_SEE_OTHER,
        )


@app.get("/workout_templates/{template_id}", response_model=list[WorkoutTemplate])
def get_workout_template(request: Request, template_id: int):
    with Session(engine) as session:
        workout_template = session.exec(
            select(WorkoutTemplate).where(WorkoutTemplate.id == template_id)
        ).one()

        exercises = session.exec(select(Exercise)).all()
        return templates.TemplateResponse(
            request=request,
            name="workout_template.html",
            context={"workout_template": workout_template, "exercises": exercises},
        )


# Template Exercise
@app.post("/template_exercises/", response_model=TemplateExercise)
# def create_template_exercise(workout_templatetemplate_exercise: TemplateExercise):
def create_template_exercise(
    workout_template_id: Annotated[int, Form()],
    exercise_id: Annotated[int, Form()],
):
    template_exercise = TemplateExercise(
        workout_template_id=workout_template_id,
        exercise_id=exercise_id,
    )

    with Session(engine) as session:
        session.add(template_exercise)
        session.commit()
        session.refresh(template_exercise)

        return RedirectResponse(
            app.url_path_for(
                "get_workout_template",
                template_id=template_exercise.workout_template_id,
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )


# TODO: Change to DELETE method for REST/AJAX
@app.post("/template_exercises/{template_exercise_id}/delete")
def delete_template_exercise(template_exercise_id: int):
    with Session(engine) as session:
        template_exercise = session.exec(
            select(TemplateExercise).where(TemplateExercise.id == template_exercise_id)
        ).first()

        template_id = template_exercise.workout_template_id
        print(f"Deleting template exercise {template_exercise_id}")
        session.delete(template_exercise)
        session.commit()

        return RedirectResponse(
            app.url_path_for(
                "get_workout_template",
                template_id=template_id,
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )


# TODO: Add PUT method for template_exercises for changing order

# TODO: Create workouts
# Creating workouts (selecting exercises, entering sets--weight and reps),
# viewing all workouts in program (e.g. - both calendar and list), viewing and
# updating selected workouts
# workout = select exercise enter weight, enter reps, click button to add another
# exercise (JS) OR just have 6-8 entries and only use what is actually entered


# Workout
@app.post("/workouts/", response_model=Workout)
def create_workout(template_id: Annotated[str, Form()]):
    workout = Workout(template_id=template_id, date=date.today())
    with Session(engine) as session:
        session.add(workout)
        session.commit()
        session.refresh(workout)

        workout_template = session.exec(
            select(WorkoutTemplate).where(WorkoutTemplate.id == template_id)
        ).one()

        for exercise in workout_template.exercises:
            workout_exercise = WorkoutExercise(
                workout_id=workout.id, exercise_id=exercise.id
            )
            session.add(workout_exercise)

        session.commit()

        return RedirectResponse(
            app.url_path_for("get_workout", template_id=workout.id),
            status_code=status.HTTP_303_SEE_OTHER,
        )


# @app.post("/workouts/", response_model=Workout)
# def create_workout(workout: Workout):
#     workout = Workout(template_id=template_id, date=date.today())
#     with Session(engine) as session:
#         session.add(workout)
#         session.commit()
#         session.refresh(workout)
#
#         return workout


@app.put("/workouts/{workout_id}", response_model=Workout)
def update_workout(template_id: int, date: str, workout_id: int):
    with Session(engine) as session:
        workout = session.exec(select(Workout).where(Workout.id == workout_id)).one()

        workout.template_id = template_id
        workout.date = date
        session.add(workout)
        session.commit()
        session.refresh(workout)

        # return workout
        return RedirectResponse(
            app.url_path_for("get_workout", template_id=workout.id),
            status_code=status.HTTP_303_SEE_OTHER,
        )


@app.get("/workouts/", response_model=list[Workout])
def get_workouts(request: Request):
    with Session(engine) as session:
        workouts = session.exec(select(Workout)).all()
        programs = session.exec(select(Program)).all()

        return workouts


@app.get("/workouts/{workout_id}", response_model=Workout)
def get_workout(request: Request, workout_id: int):
    with Session(engine) as session:
        workout = session.exec(select(Workout).where(Workout.id == workout_id)).one()

        # return workout
        return templates.TemplateResponse(
            request=request,
            name="workout.html",
            context={"workout": workout},
        )


# MuscleGroup
@app.post("/muscle_groups/", response_model=MuscleGroup)
def create_muscle_group(muscle_group: MuscleGroup):
    with Session(engine) as session:
        session.add(muscle_group)
        session.commit()
        session.refresh(muscle_group)
        return muscle_group


@app.get("/muscle_groups/", response_model=list[MuscleGroup])
def get_muscle_groups():
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
def get_muscles():
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
def get_exercises():
    with Session(engine) as session:
        exercises = session.exec(select(Exercise)).all()
        return exercises


# WorkoutExercise
@app.post("/workout_exercises/", response_model=WorkoutExercise)
def create_workout_exercise(workout_exercise: WorkoutExercise):
    with Session(engine) as session:
        session.add(workout_exercise)
        session.commit()
        session.refresh(workout_exercise)
        return workout_exercise


@app.get("/workout_exercises/", response_model=list[WorkoutExercise])
def get_workout_exercises(workout_id: int = None):
    with Session(engine) as session:
        # TODO: Add query param for workout_id
        # workout_exercises = session.exec(select(WorkoutExercise).where(
        #     WorkoutExercise.workout_id == workout_id)
        # ).all()
        workout_exercises = session.exec(select(WorkoutExercise)).all()
        return workout_exercises


@app.get("/workout_exercises/{workout_exercise_id}", response_model=WorkoutExercise)
# def get_workout_exercise(workout_exercise_id: int):
def get_workout_exercise(request: Request, workout_exercise_id: int):
    with Session(engine) as session:
        workout_exercise = session.exec(
            select(WorkoutExercise).where(WorkoutExercise.id == workout_exercise_id)
        ).one()

        # return workout_exercise
        return templates.TemplateResponse(
            request=request,
            name="workout_exercise.html",
            context={"workout_exercise": workout_exercise},
        )


# WorkoutSet
@app.post("/workout_sets/", response_model=WorkoutSet)
def create_user(workout_set: WorkoutSet):
    with Session(engine) as session:
        session.add(workout_set)
        session.commit()
        session.refresh(workout_set)
        return workout_set


@app.get("/workout_sets/", response_model=list[WorkoutSet])
def get_users():
    with Session(engine) as session:
        workout_sets = session.exec(select(WorkoutSet)).all()
        return workout_sets


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
