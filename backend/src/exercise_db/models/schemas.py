from datetime import date, datetime

from sqlmodel import Field, SQLModel


class ProgramTypeBase(SQLModel):
    name: str


class ProgramTypeCreate(ProgramTypeBase):
    pass


class ProgramTypeRead(ProgramTypeBase):
    id: int


class ProgramBaseSchema(SQLModel):
    name: str
    start_date: date
    description: str | None = None
    program_type_id: int | None = None


class ProgramCreate(ProgramBaseSchema):
    pass


class ProgramUpdate(ProgramBaseSchema):
    pass


class ProgramRead(ProgramBaseSchema):
    id: int


class MuscleGroupBase(SQLModel):
    name: str


class MuscleGroupCreate(MuscleGroupBase):
    pass


class MuscleGroupRead(MuscleGroupBase):
    id: int


class MuscleBaseSchema(SQLModel):
    name: str
    muscle_group_id: int | None = None


class MuscleCreate(MuscleBaseSchema):
    pass


class MuscleRead(MuscleBaseSchema):
    id: int


class ExerciseBaseSchema(SQLModel):
    name: str
    is_compound: bool
    muscle_primary: int | None = None
    muscle_secondary: int | None = None


class ExerciseCreate(ExerciseBaseSchema):
    pass


class ExerciseRead(ExerciseBaseSchema):
    id: int


class WorkoutTemplateBaseSchema(SQLModel):
    day_of_week: int = Field(ge=1, le=7)
    label: str | None = None
    program_id: int | None = None


class WorkoutTemplateCreate(WorkoutTemplateBaseSchema):
    pass


class WorkoutTemplateUpdate(WorkoutTemplateBaseSchema):
    pass


class WorkoutTemplateRead(WorkoutTemplateBaseSchema):
    id: int


class TemplateExerciseBaseSchema(SQLModel):
    order: int | None = 1
    workout_template_id: int | None = None
    exercise_id: int | None = None


class TemplateExerciseCreate(TemplateExerciseBaseSchema):
    pass


class TemplateExerciseRead(TemplateExerciseBaseSchema):
    id: int


class UserBase(SQLModel):
    user_name: str
    last_name: str
    first_name: str
    email: str
    creation_date: datetime | None = None
    last_login_date: datetime | None = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class WorkoutBaseSchema(SQLModel):
    program_id: int | None = None
    template_id: int | None = None
    date: date
    duration: int | None = None


class WorkoutCreate(WorkoutBaseSchema):
    pass


class WorkoutUpdate(WorkoutBaseSchema):
    pass


class WorkoutRead(WorkoutBaseSchema):
    id: int


class WorkoutExerciseBaseSchema(SQLModel):
    order: int = 1
    notes: str | None = None
    workout_id: int | None = None
    exercise_id: int | None = None


class WorkoutExerciseCreate(WorkoutExerciseBaseSchema):
    pass


class WorkoutExerciseUpdate(WorkoutExerciseBaseSchema):
    pass


class WorkoutExerciseRead(WorkoutExerciseBaseSchema):
    id: int


class ExerciseSetBaseSchema(SQLModel):
    set_number: int
    weight: int
    reps: int
    workout_exercise_id: int | None = None


class ExerciseSetCreate(ExerciseSetBaseSchema):
    pass


class ExerciseSetUpdate(ExerciseSetBaseSchema):
    pass


class ExerciseSetRead(ExerciseSetBaseSchema):
    id: int


class WorkoutExerciseDetailRead(WorkoutExerciseRead):
    sets: list[ExerciseSetRead] = []


class WorkoutDetailRead(WorkoutRead):
    exercises: list[WorkoutExerciseDetailRead] = []
