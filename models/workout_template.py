from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.program import Program
    from models.template_exercise import TemplateExercise


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
    # workouts: list["Workout"] = Relationship(
    #     back_populates="template",
    #     sa_relationship_kwargs=dict(lazy="selectin"),
    # )
