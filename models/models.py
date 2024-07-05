from datetime import datetime

from sqlmodel import Field, Session, SQLModel, create_engine, select


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_name: str
    last_name: str
    first_name: str
    email: str
    creation_date: datetime | None
    last_login_date: datetime | None


class Program(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    program_name: str


class Workout(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    program_id: int | None = Field(default=None, foreign_key="program.id")
    date: datetime


class MuscleGroup(SQLModel, table=True):
    __tablename__ = "muscle_group"
    id: int | None = Field(default=None, primary_key=True)
    group_name: str


class Muscle(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    muscle_name: str
    muscle_group_id: int | None = Field(default=None, foreign_key="muscle_group.id")


class Exercise(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    exercise_name: str
    muscle_primary: int | None = Field(default=None, foreign_key="muscle.id")
    muscle_secondary: int | None = Field(default=None, foreign_key="muscle.id")
    is_compound: bool


class EmgActivation(SQLModel, table=True):
    __tablename__ = "emg_activation"
    id: int | None = Field(default=None, primary_key=True)
    muscle: int | None = Field(default=None, foreign_key="muscle.id")
    exercise: int | None = Field(default=None, foreign_key="exercise.id")
    activation: int


class UserExercise(SQLModel, table=True):
    __tablename__ = "user_exercise"
    id: int | None = Field(default=None, primary_key=True)
    workout_id: int | None = Field(default=None, foreign_key="workout.id")
    exercise_id: int | None = Field(default=None, foreign_key="exercise.id")
    sets: int


class UserSet(SQLModel, table=True):
    __tablename__ = "user_set"
    id: int | None = Field(default=None, primary_key=True)
    user_exercise_id: int | None = Field(default=None, foreign_key="user_exercise.id")
    set_number: int
    weight: int
    reps: int
