from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.models import ExerciseSet
from models.schemas import ExerciseSetRead, ExerciseSetUpdate
from shared.utils.database import engine

router = APIRouter(
    prefix="/exercise_sets",
    tags=["exercise_sets"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{exercise_set_id}", response_model=ExerciseSetRead)
def get_exercise_set(exercise_set_id: int):
    with Session(engine) as session:
        exercise_set = session.exec(
            select(ExerciseSet).where(ExerciseSet.id == exercise_set_id)
        ).first()

        if exercise_set is None:
            raise HTTPException(status_code=404, detail="Exercise set not found")

        return exercise_set


@router.put("/{exercise_set_id}", response_model=ExerciseSetRead)
def update_exercise_set(exercise_set_id: int, exercise_set: ExerciseSetUpdate):
    with Session(engine) as session:
        db_exercise_set = session.get(ExerciseSet, exercise_set_id)

        if db_exercise_set is None:
            raise HTTPException(status_code=404, detail="Exercise set not found")

        exercise_set_data = exercise_set.model_dump(exclude_unset=True)
        for key, value in exercise_set_data.items():
            setattr(db_exercise_set, key, value)

        session.add(db_exercise_set)
        session.commit()
        session.refresh(db_exercise_set)

        return db_exercise_set


@router.delete("/{exercise_set_id}", status_code=204)
def delete_exercise_set(exercise_set_id: int):
    with Session(engine) as session:
        exercise_set = session.get(ExerciseSet, exercise_set_id)

        if not exercise_set:
            raise HTTPException(status_code=404, detail="Exercise set not found")

        session.delete(exercise_set)
        session.commit()
