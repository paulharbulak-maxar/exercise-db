from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.program import Program


class ProgramType(SQLModel, table=True):
    __tablename__ = "program_type"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    programs: list["Program"] = Relationship(
        back_populates="program_type",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
