from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from models.emg_activation import EmgActivation
from models.muscle import Muscle


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
        # back_populates="exercise",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
