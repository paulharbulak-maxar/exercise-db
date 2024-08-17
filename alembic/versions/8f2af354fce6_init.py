"""init

Revision ID: 8f2af354fce6
Revises: 
Create Date: 2024-07-02 16:16:50.094415

"""

import csv
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from sqlmodel import Session

from alembic import context, op
from models.models import (
    Exercise,
    Muscle,
    MuscleGroup,
    Program,
    ProgramType,
    TemplateExercise,
    User,
    Workout,
    WorkoutExercise,
    WorkoutSet,
    WorkoutTemplate,
)

# revision identifiers, used by Alembic.
revision: str = "8f2af354fce6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def insert_records(engine):  # exercise_table
    with Session(engine) as session:
        admin_user = User(
            user_name="admin",
            last_name="Harbulak",
            first_name="Paul",
            email="paul.harbulak@gmail.com",
            creation_date=datetime.now(),
            last_login_date=datetime.now(),
        )

        session.add(admin_user)
        session.commit()

        upper_lower = ProgramType(name="Upper/Lower")
        program_types = [
            upper_lower,
            ProgramType(name="Push/Pull/Legs"),
            ProgramType(name="3-day split"),
            ProgramType(name="4-day split"),
            ProgramType(name="5-day split"),
            ProgramType(name="HLM"),
            ProgramType(name="Starting Strength"),
            ProgramType(name="Texas Method"),
            ProgramType(name="5/3/1"),
            ProgramType(name="Westside"),
            ProgramType(name="RTS Gen. Intermediate"),
            ProgramType(name="HST"),
        ]

        for p in program_types:
            session.add(p)

        legs = MuscleGroup(group_name="legs")
        arms = MuscleGroup(group_name="arms")
        chest = MuscleGroup(group_name="chest")
        back = MuscleGroup(group_name="back")
        shoulders = MuscleGroup(group_name="shoulders")
        core = MuscleGroup(group_name="core")

        muscle_groups = [legs, arms, chest, back, shoulders, core]
        for mg in muscle_groups:
            session.add(mg)

        session.commit()

        quads = Muscle(muscle_name="quadriceps", muscle_group_id=legs.id)
        hamstrings = Muscle(muscle_name="hamstrings", muscle_group_id=legs.id)
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
            hamstrings,
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

        for m in muscles:
            session.add(m)

        session.commit()

        bench_press = Exercise(
            name="Bench Press",
            muscle_primary=pecs.id,
            muscle_secondary=triceps.id,
            is_compound=True,
        )
        ohp = Exercise(
            name="Overhead Press",
            muscle_primary=front_delt.id,
            muscle_secondary=side_delt.id,
            is_compound=True,
        )
        inc_db_bp = Exercise(
            name="Incline Dumbbell Bench Press",
            muscle_primary=pecs.id,
            muscle_secondary=shoulders.id,
            is_compound=True,
        )
        cg_bp = Exercise(
            name="Close-grip Bench Press",
            muscle_primary=chest.id,
            muscle_secondary=triceps.id,
            is_compound=True,
        )
        pull_ups = Exercise(
            name="Pull-ups",
            muscle_primary=lats.id,
            muscle_secondary=rhomboids.id,
            is_compound=True,
        )
        chin_ups = Exercise(
            name="Chin-ups",
            muscle_primary=lats.id,
            muscle_secondary=rhomboids.id,
            is_compound=True,
        )
        db_row = Exercise(
            name="Dumbbell Row",
            muscle_primary=lats.id,
            muscle_secondary=rhomboids.id,
            is_compound=True,
        )
        bb_row = Exercise(
            name="Barbell Row",
            muscle_primary=lats.id,
            muscle_secondary=rhomboids.id,
            is_compound=True,
        )
        hammer_curl = Exercise(
            name="Hammer Curl",
            muscle_primary=brachialis.id,
            muscle_secondary=biceps.id,
            is_compound=False,
        )
        pre_curl = Exercise(
            name="Preacher Curl", muscle_primary=biceps.id, is_compound=False
        )
        squat = Exercise(
            name="Squat",
            muscle_primary=quads.id,
            muscle_secondary=glutes.id,
            is_compound=True,
        )
        sumo_dl = Exercise(
            name="Sumo Deadlift",
            muscle_primary=glutes.id,
            muscle_secondary=hamstrings.id,
            is_compound=True,
        )
        sl_dl = Exercise(
            name="Straight-leg Deadlift",
            muscle_primary=glutes.id,
            muscle_secondary=hamstrings.id,
            is_compound=True,
        )
        fr_sq = Exercise(
            name="Front Squat",
            muscle_primary=quads.id,
            muscle_secondary=glutes.id,
            is_compound=True,
        )
        leg_curl = Exercise(
            name="Lying Leg Curl", muscle_primary=biceps_femoris.id, is_compound=False
        )
        hang_lr = Exercise(
            name="Hanging Leg Raise", muscle_primary=abdominals.id, is_compound=False
        )
        sit_ups = Exercise(
            name="Sit-up", muscle_primary=abdominals.id, is_compound=False
        )

        exercises = [
            bench_press,
            inc_db_bp,
            ohp,
            pull_ups,
            chin_ups,
            db_row,
            bb_row,
            sl_dl,
            sumo_dl,
            pre_curl,
            hammer_curl,
            cg_bp,
            squat,
            fr_sq,
            leg_curl,
            sit_ups,
            hang_lr,
        ]

        for exercise in exercises:
            session.add(exercise)

        exercises = [
            ("Dumbbell Bench Press", pecs.id, triceps.id, True),
            ("Incline Bench Press", pecs.id, shoulders.id, True),
            ("Decline Bench Press", pecs.id, triceps.id, True),
            ("Decline Dumbbell Bench Press", pecs.id, triceps.id, True),
            ("Board Press", pecs.id, triceps.id, True),
            ("Floor Press", pecs.id, triceps.id, True),
            ("Dumbbell Floor Press", pecs.id, triceps.id, True),
            ("Band Bench Press", pecs.id, triceps.id, True),
            ("Reverse Band Bench Press", pecs.id, triceps.id, True),
            ("Chain Bench Press", pecs.id, triceps.id, True),
            ("Dumbbell Fly", pecs.id, None, False),
            ("Incline Dumbbell Fly", pecs.id, None, False),
            ("Decline Dumbbell Fly", pecs.id, None, False),
            ("Cable Crossover", pecs.id, None, False),
            ("Push Press", front_delt.id, side_delt.id, True),
            ("Shoulder Press Behind the Neck", side_delt.id, front_delt.id, True),
            ("Seated Shoulder Press", front_delt.id, side_delt.id, True),
            ("Dumbbell Shoulder Press", front_delt.id, side_delt.id, True),
            ("One-arm Dumbbell Shoulder Press", front_delt.id, side_delt.id, True),
            ("Landmine Press", front_delt.id, side_delt.id, True),
            ("Arnold Press", front_delt.id, side_delt.id, True),
            ("Dumbbell Side Lateral", side_delt.id, None, False),
            ("Cuban Press", side_delt.id, None, False),
            ("Rear Delt Raise", rear_delt.id, None, False),
            ("Face Pull", rear_delt.id, None, False),
            ("Front Dumbbell Raise", front_delt.id, None, False),
            ("Front Barbell Raise", front_delt.id, None, False),
            ("Front Plate Raise", front_delt.id, None, False),
            ("Upright Row", side_delt.id, rear_delt.id, True),
            ("Pulldown", lats.id, rhomboids.id, True),
            ("Barbell Pullover", lats.id, None, False),
            ("Straight-arm Pulldown", lats.id, None, False),
            ("Pulldown Behind the Neck", lats.id, rhomboids.id, True),
            ("Landmine Row", lats.id, rhomboids.id, True),
            ("One-arm Landmine Row", lats.id, rhomboids.id, True),
            ("T-bar Row", lats.id, rhomboids.id, True),
            ("Deadlift", glutes.id, hamstrings.id, True),
            ("Romainian Deadlift", glutes.id, hamstrings.id, True),
            ("Rack Pull", glutes.id, hamstrings.id, True),
            ("Deficit Deadlift", glutes.id, hamstrings.id, True),
            ("One-arm Deadlift", glutes.id, hamstrings.id, True),
            ("Good Morning", glutes.id, erectors.id, True),
            ("Seated Good Morning", glutes.id, erectors.id, True),
            ("Pull-through", glutes.id, erectors.id, True),
            ("Clean", glutes.id, erectors.id, True),
            ("Clean and Jerk", glutes.id, erectors.id, True),
            ("Snatch", glutes.id, erectors.id, True),
            ("Kettlebell Swing", glutes.id, erectors.id, True),
            ("Kettlebell Clean", glutes.id, erectors.id, True),
            ("Kettlebell Snatch", glutes.id, erectors.id, True),
            ("Turkish Get-up", glutes.id, erectors.id, True),
            ("Power Clean", glutes.id, erectors.id, True),
            ("Power Clean and Jerk", glutes.id, erectors.id, True),
            ("Dumbbell Clean and Jerk", glutes.id, erectors.id, True),
            ("Hang Clean", glutes.id, erectors.id, True),
            ("Hang Snatch", glutes.id, erectors.id, True),
            ("High Pull", glutes.id, traps.id, True),
            ("Snatch High Pull", glutes.id, traps.id, True),
            ("Barbell Shrug", traps.id, None, False),
            ("Dumbbell Shrug", traps.id, None, False),
            ("Jump Shrug", traps.id, None, False),
            ("Barbell Curl", biceps.id, None, False),
            ("Dumbbell Curl", biceps.id, None, False),
            ("Cable Curl", biceps.id, None, False),
            ("Preacher Curl", biceps.id, None, False),
            ("EZ Bar Curl", biceps.id, None, False),
            ("Spider Curl", biceps.id, None, False),
            ("Incline Dumbbell Curl", biceps.id, None, False),
            ("Drag Curl", biceps.id, None, False),
            ("Concentration Curl", biceps.id, None, False),
            ("Hammer Curl", brachialis.id, biceps.id, False),
            ("Reverse Curl", brachioradialis.id, biceps.id, False),
            ("Bench Dips", triceps.id, None, False),
            ("Dips", triceps.id, chest.id, True),
            ("Skull Crushers", triceps.id, None, False),
            ("Cable Triceps Extension", triceps.id, None, False),
            ("Incline Barbell Triceps Extension", triceps.id, None, False),
            ("Dumbbell Kickback", triceps.id, None, False),
            ("Close-grip Bench Press", chest.id, triceps.id, True),
            ("J.M. Press", triceps.id, chest.id, True),
            ("Dumbbell Triceps Extension", triceps.id, None, False),
            ("Tricep Pushdown", triceps.id, None, False),
            ("Decline Triceps Extension", triceps.id, None, False),
            ("One-arm Dumbbell Triceps Extension", triceps.id, None, False),
            ("Squat", quads.id, glutes.id, True),
            ("Front Squat", quads.id, glutes.id, True),
            ("Hack Squat", quads.id, glutes.id, True),
            ("Box Squat", quads.id, glutes.id, True),
            ("Safety Bar Squat", quads.id, glutes.id, True),
            ("Zercher Squat", quads.id, glutes.id, True),
            ("Pistol Squat", quads.id, glutes.id, True),
            ("Overhead Squat", quads.id, glutes.id, True),
            ("Goblet Squat", quads.id, glutes.id, True),
            ("Landmine Squat", quads.id, glutes.id, True),
            ("Belt Squat", quads.id, glutes.id, True),
            ("Lunge", quads.id, glutes.id, True),
            ("Reverse Lunge", quads.id, glutes.id, True),
            ("Step-up", quads.id, glutes.id, True),
            ("Leg Press", quads.id, glutes.id, True),
            ("Leg Extension", quads.id, None, False),
            ("Lying Leg Curl", biceps_femoris.id, None, False),
            ("Calf Raise", calves.id, None, False),
            ("Seated Calf Raise", calves.id, None, False),
            ("Hip Adduction Machine", adductors.id, None, False),
            ("Hip Abduction Machine", abductors.id, None, False),
            ("Crab Walk", abductors.id, None, False),
            ("Monster Walk", abductors.id, None, False),
            ("Decline Sit-up", abdominals.id, None, False),
            ("Lying Leg Raise", abdominals.id, None, False),
            ("Incline Leg Raise", abdominals.id, None, False),
            ("Roman Chair Sit-up", abdominals.id, None, False),
            ("Crunches", abdominals.id, None, False),
            ("Twisting Crunch", abdominals.id, obliques.id, False),
            ("Twisting Sit-ups", abdominals.id, obliques.id, False),
            ("Side Crunch", obliques.id, None, False),
            ("Russian Twist", obliques.id, abdominals.id, False),
            ("Side Bends", obliques.id, None, False),
            ("Back Hyperextension", erectors.id, None, False),
        ]

        for e in exercises:
            kwargs = {
                "name": e[0],
                "muscle_primary": e[1],
                "muscle_secondary": e[2],
                "is_compound": e[3],
            }

            session.add(Exercise(**kwargs))

        # session.bulk_insert_mappings(Exercise, [{}])
        session.commit()

        new_program = Program(
            name="Upper/Lower",
            program_type_id=upper_lower.id,
            start_date=datetime.now(),
            description="Sample upper/lower 4-day workout program",
        )

        session.add(new_program)
        session.commit()
        session.refresh(new_program)

        upper_a = WorkoutTemplate(
            program_id=new_program.id, day_of_week=2, label="Upper A"
        )
        lower_a = WorkoutTemplate(
            program_id=new_program.id, day_of_week=3, label="Lower A"
        )
        upper_b = WorkoutTemplate(
            program_id=new_program.id, day_of_week=5, label="Upper B"
        )
        lower_b = WorkoutTemplate(
            program_id=new_program.id, day_of_week=6, label="Lower B"
        )

        templates = [upper_a, lower_a, upper_b, lower_b]
        for temp in templates:
            session.add(temp)
            session.commit()
            session.refresh(temp)

        template_exercises = [
            TemplateExercise(
                order=1, workout_template_id=upper_a.id, exercise_id=bench_press.id
            ),
            TemplateExercise(
                order=2, workout_template_id=upper_a.id, exercise_id=inc_db_bp.id
            ),
            TemplateExercise(
                order=3, workout_template_id=upper_a.id, exercise_id=pull_ups.id
            ),
            TemplateExercise(
                order=4, workout_template_id=upper_a.id, exercise_id=db_row.id
            ),
            TemplateExercise(
                order=5, workout_template_id=upper_a.id, exercise_id=hammer_curl.id
            ),
            TemplateExercise(
                order=1, workout_template_id=lower_a.id, exercise_id=squat.id
            ),
            TemplateExercise(
                order=2, workout_template_id=lower_a.id, exercise_id=sl_dl.id
            ),
            TemplateExercise(
                order=3, workout_template_id=lower_a.id, exercise_id=leg_curl.id
            ),
            TemplateExercise(
                order=4, workout_template_id=lower_a.id, exercise_id=hang_lr.id
            ),
            TemplateExercise(
                order=1, workout_template_id=upper_b.id, exercise_id=cg_bp.id
            ),
            TemplateExercise(
                order=2, workout_template_id=upper_b.id, exercise_id=ohp.id
            ),
            TemplateExercise(
                order=3, workout_template_id=upper_b.id, exercise_id=chin_ups.id
            ),
            TemplateExercise(
                order=4, workout_template_id=upper_b.id, exercise_id=bb_row.id
            ),
            TemplateExercise(
                order=5, workout_template_id=upper_b.id, exercise_id=pre_curl.id
            ),
            TemplateExercise(
                order=1, workout_template_id=lower_b.id, exercise_id=sumo_dl.id
            ),
            TemplateExercise(
                order=2, workout_template_id=lower_b.id, exercise_id=fr_sq.id
            ),
            TemplateExercise(
                order=3, workout_template_id=lower_b.id, exercise_id=leg_curl.id
            ),
            TemplateExercise(
                order=4, workout_template_id=lower_b.id, exercise_id=sit_ups.id
            ),
        ]

        for template_ex in template_exercises:
            session.add(template_ex)

        session.commit()


def upgrade() -> None:
    print("Running migration")
    user_table = op.create_table(
        "user",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("user_name", sa.VARCHAR(), nullable=False),
        sa.Column("last_name", sa.VARCHAR(), nullable=False),
        sa.Column("first_name", sa.VARCHAR(), nullable=False),
        sa.Column("email", sa.VARCHAR(), nullable=False),
        sa.Column("creation_date", sa.DATETIME(), nullable=False),
        sa.Column("last_login_date", sa.DATETIME(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    muscle_group_table = op.create_table(
        "muscle_group",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("group_name", sa.VARCHAR(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    muscle_table = op.create_table(
        "muscle",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("muscle_name", sa.VARCHAR(), nullable=False),
        sa.Column("muscle_group_id", sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(
            ["muscle_group_id"],
            ["muscle_group.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    exercise_table = op.create_table(
        "exercise",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("muscle_primary", sa.INTEGER(), nullable=True),
        sa.Column("muscle_secondary", sa.INTEGER(), nullable=True),
        sa.Column("is_compound", sa.BOOLEAN(), nullable=False),
        sa.ForeignKeyConstraint(
            ["muscle_primary"],
            ["muscle.id"],
        ),
        sa.ForeignKeyConstraint(
            ["muscle_secondary"],
            ["muscle.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    program_type_table = op.create_table(
        "program_type",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    program_table = op.create_table(
        "program",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        # sa.Column("user_id", sa.INTEGER(), nullable=True),
        sa.Column("program_type_id", sa.INTEGER(), nullable=False),
        sa.Column("start_date", sa.DATETIME(), nullable=False),
        sa.Column("description", sa.VARCHAR(), nullable=True),
        # sa.ForeignKeyConstraint(
        #     ["user_id"],
        #     ["user.id"],
        # ),
        sa.ForeignKeyConstraint(
            ["program_type_id"],
            ["program_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    workout_template_table = op.create_table(
        "workout_template",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("program_id", sa.INTEGER(), nullable=False),
        sa.Column("label", sa.VARCHAR(), nullable=True),
        sa.Column("day_of_week", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["program_id"],
            ["program.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    template_exercise_table = op.create_table(
        "template_exercise",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("order", sa.INTEGER(), nullable=False),
        sa.Column("workout_template_id", sa.INTEGER(), nullable=False),
        sa.Column("exercise_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["workout_template_id"],
            ["workout_template.id"],
        ),
        sa.ForeignKeyConstraint(
            ["exercise_id"],
            ["exercise.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    workout_table = op.create_table(
        "workout",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("program_id", sa.INTEGER(), nullable=False),
        sa.Column("template_id", sa.INTEGER(), nullable=True),
        sa.Column("date", sa.DATETIME(), nullable=False),
        sa.ForeignKeyConstraint(
            ["program_id"],
            ["program.id"],
        ),
        sa.ForeignKeyConstraint(
            ["template_id"],
            ["workout_template.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    workout_exercise_table = op.create_table(
        "workout_exercise",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("order", sa.INTEGER(), nullable=False),
        sa.Column("workout_id", sa.INTEGER(), nullable=False),
        sa.Column("exercise_id", sa.INTEGER(), nullable=False),
        sa.Column("notes", sa.VARCHAR(), nullable=True),
        sa.ForeignKeyConstraint(
            ["exercise_id"],
            ["exercise.id"],
        ),
        sa.ForeignKeyConstraint(
            ["workout_id"],
            ["workout.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    workout_set_table = op.create_table(
        "workout_set",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("workout_exercise_id", sa.INTEGER(), nullable=True),
        sa.Column("set_number", sa.INTEGER(), nullable=False),
        sa.Column("weight", sa.INTEGER(), nullable=False),
        sa.Column("reps", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["workout_exercise_id"],
            ["workout_exercise.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    emg_activation_table = op.create_table(
        "emg_activation",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("muscle_id", sa.INTEGER(), nullable=True),
        sa.Column("exercise_id", sa.INTEGER(), nullable=True),
        sa.Column("activation", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["exercise_id"],
            ["exercise.id"],
        ),
        sa.ForeignKeyConstraint(
            ["muscle_id"],
            ["muscle.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    url = context.config.get_main_option("sqlalchemy.url")
    engine = sa.create_engine(url)
    insert_records(engine)


def downgrade() -> None:
    op.drop_table("emg_activation")
    op.drop_table("workout_exercise")
    op.drop_table("workout_set")
    op.drop_table("workout")
    op.drop_table("program_exercise")
    op.drop_table("program_workout")
    op.drop_table("program")
    op.drop_table("program_type")
    op.drop_table("exercise")
    op.drop_table("muscle")
    op.drop_table("muscle_group")
    op.drop_table("user")
