from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_name: str
    last_name: str
    first_name: str
    email: str
    creation_date: datetime | None
    last_login_date: datetime | None


class ProgramType(SQLModel, table=True):
    __tablename__ = "program_type"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    programs: list["Program"] = Relationship(
        back_populates="program_type",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class Program(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    # user_id: int | None = Field(default=None, foreign_key="user.id")
    program_type_id: int | None = Field(default=None, foreign_key="program_type.id")
    program_type: Optional["ProgramType"] = Relationship(
        back_populates="programs",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    start_date: datetime
    description: Optional[str]
    workout_templates: list["WorkoutTemplate"] = Relationship(
        back_populates="program",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class WorkoutTemplate(SQLModel, table=True):
    __tablename__ = "workout_template"
    id: int | None = Field(default=None, primary_key=True)
    program_id: int | None = Field(default=None, foreign_key="program.id")
    program: Optional["Program"] = Relationship(
        back_populates="workout_templates",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    # TODO: Limit to 1-7 & create Enum to get string from number in endpoint
    day_of_week: int
    label: str | None
    exercises: list["TemplateExercise"] = Relationship(
        # back_populates="workout_template",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class TemplateExercise(SQLModel, table=True):
    __tablename__ = "template_exercise"
    id: int | None = Field(default=None, primary_key=True)
    workout_template_id: int | None = Field(
        default=None, foreign_key="workout_template.id"
    )
    exercise_id: int | None = Field(default=None, foreign_key="exercise.id")
    exercise: Optional["Exercise"] = Relationship(
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    # TODO: Add workout order
    # order: int | None


class Workout(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    template_id: int | None = Field(default=None, foreign_key="workout_template.id")
    template: Optional["WorkoutTemplate"] = Relationship(
        # back_populates="workouts",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    date: datetime
    exercises: list["WorkoutExercise"] = Relationship(
        # back_populates="muscle_group",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class MuscleGroup(SQLModel, table=True):
    __tablename__ = "muscle_group"
    id: int | None = Field(default=None, primary_key=True)
    group_name: str
    muscles: list["Muscle"] = Relationship(
        back_populates="muscle_group",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class Muscle(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    muscle_name: str
    muscle_group_id: int | None = Field(default=None, foreign_key="muscle_group.id")
    muscle_group: Optional["MuscleGroup"] = Relationship(
        back_populates="muscles",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    primary_exercises: list["Exercise"] = Relationship(
        back_populates="primary_muscles",
        sa_relationship_kwargs=dict(
            lazy="selectin", foreign_keys="[Exercise.muscle_primary]"
        ),
    )
    secondary_exercises: list["Exercise"] = Relationship(
        back_populates="secondary_muscles",
        sa_relationship_kwargs=dict(
            lazy="selectin", foreign_keys="[Exercise.muscle_secondary]"
        ),
    )


class Exercise(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    muscle_primary: int | None = Field(default=None, foreign_key="muscle.id")
    muscle_secondary: int | None = Field(default=None, foreign_key="muscle.id")
    is_compound: bool
    primary_muscles: list["Muscle"] = Relationship(
        back_populates="primary_exercises",
        sa_relationship_kwargs=dict(
            lazy="selectin", foreign_keys="[Exercise.muscle_primary]"
        ),
    )
    secondary_muscles: list["Muscle"] = Relationship(
        back_populates="secondary_exercises",
        sa_relationship_kwargs=dict(
            lazy="selectin", foreign_keys="[Exercise.muscle_secondary]"
        ),
    )
    emg_activation: Optional["EmgActivation"] = Relationship(
        # back_populates="muscle",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class EmgActivation(SQLModel, table=True):
    __tablename__ = "emg_activation"
    id: int | None = Field(default=None, primary_key=True)
    muscle_id: int | None = Field(default=None, foreign_key="muscle.id")
    exercise_id: int | None = Field(default=None, foreign_key="exercise.id")
    activation: int


class WorkoutExercise(SQLModel, table=True):
    __tablename__ = "workout_exercise"
    id: int | None = Field(default=None, primary_key=True)
    workout_id: int | None = Field(default=None, foreign_key="workout.id")
    exercise_id: int | None = Field(default=None, foreign_key="exercise.id")
    exercise: Optional["Exercise"] = Relationship(
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    notes: str | None
    sets: list["WorkoutSet"] = Relationship(
        # back_populates="muscle_group",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class WorkoutSet(SQLModel, table=True):
    __tablename__ = "workout_set"
    id: int | None = Field(default=None, primary_key=True)
    workout_exercise_id: int | None = Field(
        default=None, foreign_key="workout_exercise.id"
    )
    set_number: int
    weight: int
    reps: int
