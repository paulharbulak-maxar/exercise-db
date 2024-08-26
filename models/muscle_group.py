from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.muscle import Muscle


class MuscleGroup(SQLModel, table=True):
    __tablename__ = "muscle_group"
    id: int | None = Field(default=None, primary_key=True)
    group_name: str
    muscles: list["Muscle"] = Relationship(
        back_populates="muscle_group",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
