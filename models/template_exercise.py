from sqlmodel import Field, Relationship, SQLModel

from models.exercise import Exercise


class TemplateExercise(SQLModel, table=True):
    __tablename__ = "template_exercise"
    id: int | None = Field(default=None, primary_key=True)
    order: int = 0
    workout_template_id: int | None = Field(
        default=None, foreign_key="workout_template.id", ondelete="CASCADE"
    )
    exercise_id: int | None = Field(default=None, foreign_key="exercise.id")
    exercise: Exercise = Relationship(
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
