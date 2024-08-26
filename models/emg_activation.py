from sqlmodel import Field, SQLModel


class EmgActivation(SQLModel, table=True):
    __tablename__ = "emg_activation"
    id: int | None = Field(default=None, primary_key=True)
    muscle_id: int | None = Field(default=None, foreign_key="muscle.id")
    exercise_id: int | None = Field(default=None, foreign_key="exercise.id")
    activation: int
