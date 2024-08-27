from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.program_type import ProgramType
    from models.workout import Workout
    from models.workout_template import WorkoutTemplate


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
