"""init

Revision ID: 8f2af354fce6
Revises: 
Create Date: 2024-07-02 16:16:50.094415

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8f2af354fce6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    print("Running migration")
    user_table = op.create_table(
        "user",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("user_name", sa.VARCHAR(), nullable=False),
        sa.Column("last_name", sa.VARCHAR(), nullable=False),
        sa.Column("first_name", sa.VARCHAR(), nullable=False),
        sa.Column("email", sa.VARCHAR(), nullable=False),
        sa.Column("creation_date", sa.TIME(), nullable=False),
        sa.Column("last_login_date", sa.TIME(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    muscle_group_table = op.create_table(
        "muscle_group",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    muscle_table = op.create_table(
        "muscle",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("muscle_group_id", sa.INTEGER(), nullable=False),
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
        sa.Column("muscle_primary", sa.INTEGER(), nullable=False),
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
        sa.Column("start_date", sa.DATE(), nullable=True),
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
        sa.Column("template_id", sa.INTEGER(), nullable=False),
        sa.Column("date", sa.DATE(), nullable=False),
        sa.Column("duration", sa.INTEGER(), nullable=True),
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
        "exercise_set",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("workout_exercise_id", sa.INTEGER(), nullable=False),
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
        sa.Column("muscle_id", sa.INTEGER(), nullable=False),
        sa.Column("exercise_id", sa.INTEGER(), nullable=False),
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


def downgrade() -> None:
    op.drop_table("emg_activation")
    op.drop_table("workout_exercise")
    op.drop_table("exercise_set")
    op.drop_table("workout")
    op.drop_table("program_exercise")
    op.drop_table("program_workout")
    op.drop_table("program")
    op.drop_table("program_type")
    op.drop_table("exercise")
    op.drop_table("muscle")
    op.drop_table("muscle_group")
    op.drop_table("user")
