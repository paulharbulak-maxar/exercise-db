from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.exercise import Exercise
    from models.exercise_set import ExerciseSet
    from models.workout import Workout


class WorkoutExercise(SQLModel, table=True):
    __tablename__ = "workout_exercise"
    id: int | None = Field(default=None, primary_key=True)
    order: int = 0
    workout_id: int | None = Field(default=None, foreign_key="workout.id")
    workout: Optional["Workout"] = Relationship(
        back_populates="exercises",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    exercise_id: int | None = Field(default=None, foreign_key="exercise.id")
    exercise: Optional["Exercise"] = Relationship(
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
    notes: str | None
    sets: list["ExerciseSet"] = Relationship(
        back_populates="workout_exercise",
        sa_relationship_kwargs=dict(lazy="selectin"),
    )
