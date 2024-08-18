import csv
from datetime import datetime

from sqlmodel import Session, select

from models.models import (
    Exercise,
    ExerciseSet,
    Muscle,
    MuscleGroup,
    Program,
    User,
    Workout,
    WorkoutExercise,
)


def insert_records(engine):
    admin_user = User(
        user_name="admin",
        last_name="Harbulak",
        first_name="Paul",
        email="paul.harbulak@gmail.com",
        creation_date=datetime.now(),
        last_login_date=datetime.now(),
    )

    programs = [
        Program(user_id=admin_user.id, program_name="Upper/Lower"),
        Program(user_id=admin_user.id, program_name="Push/Pull/Legs"),
        Program(user_id=admin_user.id, program_name="3-day split"),
        Program(user_id=admin_user.id, program_name="4-day split"),
        Program(user_id=admin_user.id, program_name="5-day split"),
        Program(user_id=admin_user.id, program_name="HLM"),
        Program(user_id=admin_user.id, program_name="Starting Strength"),
        Program(user_id=admin_user.id, program_name="Texas Method"),
        Program(user_id=admin_user.id, program_name="5/3/1"),
        Program(user_id=admin_user.id, program_name="Westside"),
        Program(user_id=admin_user.id, program_name="RTS Gen. Intermediate"),
        Program(user_id=admin_user.id, program_name="HST"),
    ]

    legs = MuscleGroup(group_name="legs")
    arms = MuscleGroup(group_name="arms")
    chest = MuscleGroup(group_name="chest")
    back = MuscleGroup(group_name="back")
    shoulders = MuscleGroup(group_name="shoulders")
    core = MuscleGroup(group_name="core")

    muscle_groups = [legs, arms, chest, back, shoulders, core]

    quads = Muscle(muscle_name="quadriceps", muscle_group_id=legs.id)
    hams = Muscle(muscle_name="hamstrings", muscle_group_id=legs.id)
    biceps_femoris = Muscle(muscle_name="biceps femoris", muscle_group_id=legs.id)
    glutes = Muscle(muscle_name="glutes", muscle_group_id=legs.id)
    calves = Muscle(muscle_name="calves", muscle_group_id=legs.id)
    adductors = Muscle(muscle_name="adductors", muscle_group_id=legs.id)
    abductors = Muscle(muscle_name="abductors", muscle_group_id=legs.id)
    triceps = Muscle(muscle_name="triceps", muscle_group_id=arms.id)
    biceps = Muscle(muscle_name="biceps", muscle_group_id=arms.id)
    brachialis = Muscle(muscle_name="brachialis", muscle_group_id=arms.id)
    brachioradialis = Muscle(muscle_name="brachioradialis", muscle_group_id=arms.id)
    pecs = Muscle(muscle_name="pectoralis", muscle_group_id=chest.id)
    lats = Muscle(muscle_name="latissimus dorsi", muscle_group_id=back.id)
    traps = Muscle(muscle_name="trapezius", muscle_group_id=back.id)
    rhomboids = Muscle(muscle_name="rhomboids", muscle_group_id=back.id)
    front_delt = Muscle(muscle_name="front deltoid", muscle_group_id=shoulders.id)
    side_delt = Muscle(muscle_name="side deltoid", muscle_group_id=shoulders.id)
    rear_delt = Muscle(muscle_name="rear deltoid", muscle_group_id=shoulders.id)
    abdominals = Muscle(muscle_name="abdominals", muscle_group_id=core.id)
    obliques = Muscle(muscle_name="obliques", muscle_group_id=core.id)
    erectors = Muscle(muscle_name="erector spinae", muscle_group_id=core.id)
    serratus = Muscle(muscle_name="serratus anterior", muscle_group_id=core.id)

    muscles = [
        quads,
        hams,
        biceps_femoris,
        glutes,
        calves,
        adductors,
        abductors,
        triceps,
        biceps,
        brachialis,
        brachioradialis,
        pecs,
        lats,
        traps,
        rhomboids,
        front_delt,
        side_delt,
        rear_delt,
        abdominals,
        obliques,
        erectors,
        serratus,
    ]

    exercises = []
    field_names = ["exercise_name", "muscle_primary", "muscle_secondary", "is_compound"]
    with open("models/exercises.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=field_names)
        for row in reader:
            exercises.append(
                Exercise(
                    exercise_name=row["exercise_name"],
                    muscle_primary=row["muscle_primary"],
                    muscle_secondary=row["muscle_secondary"],
                    is_compound=bool(row["is_compound"]),
                )
            )

    with Session(engine) as session:
        session.add(admin_user)
        for p in programs:
            session.add(p)

        for mg in muscle_groups:
            session.add(mg)

        for m in muscles:
            session.add(m)

        for e in exercises:
            session.add(e)

        session.commit()
