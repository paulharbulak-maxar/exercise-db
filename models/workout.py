from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from models.program import Program
from models.workout_template import WorkoutTemplate

if TYPE_CHECKING:
    from models.workout_exercise import WorkoutExercise


class Workout(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # TODO: Figure out how to create relationship thru another relationship (program -> template -> workout)
    program_id: int | None = Field(default=None, foreign_key="program.id")
    program: Program = Relationship(
        back_populates="workouts",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    template_id: int | None = Field(default=None, foreign_key="workout_template.id")
    template: WorkoutTemplate = Relationship(
        # back_populates="workouts",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    date: datetime
    duration: int | None
    exercises: list["WorkoutExercise"] = Relationship(
        back_populates="workout",
        sa_relationship_kwargs=dict(
            lazy="selectin",
            cascade="all, delete",
            passive_deletes=True,
        ),
    )
