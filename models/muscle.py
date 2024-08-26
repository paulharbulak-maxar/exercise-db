from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.exercise import Exercise
    from models.muscle_group import MuscleGroup


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
