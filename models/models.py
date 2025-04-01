from datetime import date, datetime
from typing import Optional

from pydantic import computed_field
from sqlmodel import Field, Relationship, SQLModel


def get_day_of_week(day: int) -> str:
    return (
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    )[day]


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_name: str
    last_name: str
    first_name: str
    email: str
    creation_date: datetime | None
    last_login_date: datetime | None


class ProgramTypeBase(SQLModel):
    name: str


class ProgramType(ProgramTypeBase, table=True):
    __tablename__ = "program_type"
    id: int | None = Field(default=None, primary_key=True)
    programs: list["Program"] = Relationship(
        back_populates="program_type",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class ProgramTypeResponse(ProgramTypeBase):
    id: int


class ProgramBase(SQLModel):
    name: str
    # user_id: int | None = Field(default=None, foreign_key="user.id")
    start_date: date
    description: str | None
    program_type_id: int | None = Field(default=None, foreign_key="program_type.id")


class Program(ProgramBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    program_type: ProgramType | None = Relationship(
        back_populates="programs",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    workout_templates: list["WorkoutTemplate"] = Relationship(
        back_populates="program",
        sa_relationship_kwargs=dict(
            lazy="selectin",
            cascade="all, delete",
            passive_deletes=True,
        ),
    )
    workouts: list["Workout"] = Relationship(
        back_populates="program",
        sa_relationship_kwargs=dict(
            lazy="selectin",
            cascade="all, delete",
            passive_deletes=True,
        ),
    )


class ProgramResponse(ProgramBase):
    id: int


class EmgActivationBase(SQLModel):
    muscle_id: int | None = Field(default=None, foreign_key="muscle.id")
    exercise_id: int | None = Field(default=None, foreign_key="exercise.id")
    activation: int


class EmgActivation(EmgActivationBase, table=True):
    __tablename__ = "emg_activation"
    id: int | None = Field(default=None, primary_key=True)


class EmgActivationResponse(EmgActivationBase):
    id: int


class MuscleGroupBase(SQLModel):
    name: str


class MuscleGroup(MuscleGroupBase, table=True):
    __tablename__ = "muscle_group"
    id: int | None = Field(default=None, primary_key=True)
    muscles: list["Muscle"] = Relationship(
        back_populates="muscle_group",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class MuscleGroupResponse(MuscleGroupBase):
    id: int


class MuscleBase(SQLModel):
    name: str
    muscle_group_id: int | None = Field(default=None, foreign_key="muscle_group.id")


class Muscle(MuscleBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    muscle_group: MuscleGroup = Relationship(
        back_populates="muscles",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    primary_exercises: list["Exercise"] = Relationship(
        back_populates="primary_muscle",
        sa_relationship_kwargs=dict(
            lazy="selectin", foreign_keys="[Exercise.muscle_primary]"
        ),
    )
    secondary_exercises: list["Exercise"] = Relationship(
        back_populates="secondary_muscle",
        sa_relationship_kwargs=dict(
            lazy="selectin", foreign_keys="[Exercise.muscle_secondary]"
        ),
    )


class MuscleResponse(MuscleBase):
    id: int


class ExerciseBase(SQLModel):
    name: str
    is_compound: bool
    muscle_primary: int | None = Field(default=None, foreign_key="muscle.id")
    muscle_secondary: int | None = Field(default=None, foreign_key="muscle.id")


class Exercise(ExerciseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    primary_muscle: Muscle = Relationship(
        back_populates="primary_exercises",
        sa_relationship_kwargs=dict(
            lazy="selectin", foreign_keys="[Exercise.muscle_primary]"
        ),
    )
    secondary_muscle: Muscle = Relationship(
        back_populates="secondary_exercises",
        sa_relationship_kwargs=dict(
            lazy="selectin", foreign_keys="[Exercise.muscle_secondary]"
        ),
    )
    emg_activation: Optional[EmgActivation] = Relationship(
        # back_populates="exercise",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class ExerciseResponse(ExerciseBase):
    id: int


class TemplateExerciseBase(SQLModel):
    order: int | None = 1
    workout_template_id: int | None = Field(
        default=None, foreign_key="workout_template.id", ondelete="CASCADE"
    )
    exercise_id: int | None = Field(default=None, foreign_key="exercise.id")


class TemplateExercise(TemplateExerciseBase, table=True):
    __tablename__ = "template_exercise"
    id: int | None = Field(default=None, primary_key=True)
    exercise: Exercise = Relationship(
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class TemplateExerciseResponse(TemplateExerciseBase):
    id: int


class WorkoutTemplateBase(SQLModel):
    day_of_week: int = Field(ge=1, le=7)
    label: str | None
    program_id: int | None = Field(
        default=None, foreign_key="program.id", ondelete="CASCADE"
    )


class WorkoutTemplate(WorkoutTemplateBase, table=True):
    __tablename__ = "workout_template"
    id: int | None = Field(default=None, primary_key=True)
    program: Program = Relationship(
        back_populates="workout_templates",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    exercises: list[TemplateExercise] = Relationship(
        # back_populates="workout_template",
        sa_relationship_kwargs=dict(
            lazy="selectin",
            cascade="all, delete",
            passive_deletes=True,
        ),
    )
    # Keep this in case it's needed for future functionality to retrieve workouts
    # workouts: list[Workout] = Relationship(
    #     back_populates="template",
    #     sa_relationship_kwargs=dict(lazy="selectin"),
    # )


class WorkoutTemplateResponse(WorkoutTemplateBase):
    id: int


class ExerciseSetBase(SQLModel):
    set_number: int
    weight: int
    reps: int
    workout_exercise_id: int | None = Field(
        default=None, foreign_key="workout_exercise.id", ondelete="CASCADE"
    )


class ExerciseSet(ExerciseSetBase, table=True):
    __tablename__ = "exercise_set"
    id: int | None = Field(default=None, primary_key=True)
    workout_exercise: "WorkoutExercise" = Relationship(
        back_populates="sets",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )


class ExerciseSetResponse(ExerciseSetBase):
    id: int


class WorkoutExerciseBase(SQLModel):
    order: int = 1
    notes: str | None
    workout_id: int | None = Field(
        default=None, foreign_key="workout.id", ondelete="CASCADE"
    )
    exercise_id: int | None = Field(default=None, foreign_key="exercise.id")


class WorkoutExercise(WorkoutExerciseBase, table=True):
    __tablename__ = "workout_exercise"
    id: int | None = Field(default=None, primary_key=True)
    workout: "Workout" = Relationship(
        back_populates="exercises",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    exercise: Exercise = Relationship(
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    sets: list[ExerciseSet] = Relationship(
        back_populates="workout_exercise",
        sa_relationship_kwargs=dict(
            lazy="selectin",
            cascade="all, delete",
            passive_deletes=True,
        ),
    )


class WorkoutExerciseResponse(WorkoutExerciseBase):
    id: int
    # exercise: ExerciseResponse


class WorkoutBase(SQLModel):
    # TODO: Figure out how to create relationship thru another relationship (program -> template -> workout)
    program_id: int | None = Field(default=None, foreign_key="program.id")
    template_id: int | None = Field(default=None, foreign_key="workout_template.id")
    date: date
    duration: int | None


class Workout(WorkoutBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    program: Program = Relationship(
        back_populates="workouts",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    template: WorkoutTemplate = Relationship(
        # back_populates="workouts",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    exercises: list[WorkoutExercise] = Relationship(
        back_populates="workout",
        sa_relationship_kwargs=dict(
            lazy="selectin",
            cascade="all, delete",
            passive_deletes=True,
        ),
    )


class WorkoutResponse(WorkoutBase):
    id: int
