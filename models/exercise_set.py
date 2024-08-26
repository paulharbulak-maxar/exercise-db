from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.workout_exercise import WorkoutExercise


class ExerciseSet(SQLModel, table=True):
    __tablename__ = "exercise_set"
    id: int | None = Field(default=None, primary_key=True)
    workout_exercise_id: int | None = Field(
        default=None, foreign_key="workout_exercise.id"
    )
    workout_exercise: list["WorkoutExercise"] = Relationship(
        back_populates="sets",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    set_number: int
    weight: int
    reps: int
