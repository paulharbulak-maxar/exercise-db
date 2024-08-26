from sqlmodel import select


def update_exercise_order(session, workout_exercise, order, foreign_key="workout_id"):
    model = workout_exercise.__class__
    other_exercises = session.exec(
        select(model)
        .where(getattr(model, "id") != workout_exercise.id)
        .where(getattr(model, foreign_key) == getattr(workout_exercise, foreign_key))
    ).all()

    for ex in other_exercises:
        if order <= ex.order < workout_exercise.order:
            ex.order += 1
        elif order >= ex.order > workout_exercise.order:
            ex.order -= 1

        session.add(ex)

    return session


# This is used to increment order of later exercises when new exercise is added
def increment_exercise_order(session, model, workout_id, order):
    exercises_after = session.exec(
        select(model)
        .where(getattr(model, "id") != workout_id)
        .where(getattr(model, "order") >= order)
    ).all()

    for ex in exercises_after:
        ex.order += 1
        session.add(ex)


# This is used to decrement order of later exercises when exercise is deleted
def decrement_exercise_order(session, workout_exercise, foreign_key="workout_id"):
    model = workout_exercise.__class__
    exercises_after = session.exec(
        select(model)
        .where(getattr(model, "id") != workout_exercise.id)
        .where(getattr(model, foreign_key) == getattr(workout_exercise, foreign_key))
        .where(getattr(model, "order") > workout_exercise.order)
    ).all()

    for ex in exercises_after:
        ex.order -= 1
        session.add(ex)
