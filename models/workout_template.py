from sqlmodel import Field, Relationship, SQLModel

from models.program import Program
from models.template_exercise import TemplateExercise


class WorkoutTemplate(SQLModel, table=True):
    __tablename__ = "workout_template"
    id: int | None = Field(default=None, primary_key=True)
    program_id: int | None = Field(
        default=None, foreign_key="program.id", ondelete="CASCADE"
    )
    program: Program = Relationship(
        back_populates="workout_templates",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    # TODO: Limit to 1-7 & create Enum to get string from number in endpoint
    day_of_week: int
    label: str | None
    exercises: list["TemplateExercise"] = Relationship(
        # back_populates="workout_template",
        sa_relationship_kwargs=dict(
            lazy="selectin",
            cascade="all, delete",
            passive_deletes=True,
        ),
    )
    # Keep this in case it's needed for future functionality to retrieve workouts
    # workouts: list["Workout"] = Relationship(
    #     back_populates="template",
    #     sa_relationship_kwargs=dict(lazy="selectin"),
    # )
