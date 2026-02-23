"""
Test configuration and fixtures for the exercise-db test suite.

This module provides pytest fixtures for database setup and FastAPI TestClient
following the patterns from FastAPI's official documentation.
"""

from datetime import date, datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from exercise_db.main import app

# Import all models to ensure they're registered with SQLModel metadata
from exercise_db.models.models import (  # noqa: F401
    EmgActivation,
    Exercise,
    ExerciseSet,
    Muscle,
    MuscleGroup,
    Program,
    ProgramType,
    TemplateExercise,
    User,
    Workout,
    WorkoutExercise,
    WorkoutTemplate,
)


@pytest.fixture(name="session")
def session_fixture():
    """
    Create a fresh SQLite in-memory database for each test.

    This fixture:
    - Creates an in-memory SQLite database
    - Creates all tables from SQLModel metadata
    - Yields a session for the test to use
    - Automatically cleans up after the test

    Following FastAPI's testing documentation pattern.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client", autouse=False)
def client_fixture(monkeypatch):
    """
    Create a FastAPI TestClient with a test database.

    This fixture:
    - Creates a fresh SQLite in-memory database for each test
    - Patches all router modules to use the test database engine
    - Creates a TestClient for making API requests
    - Automatically cleans up after the test

    Following FastAPI's dependency override pattern from the docs.
    """
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(test_engine)

    monkeypatch.setattr("exercise_db.shared.utils.database.engine", test_engine)
    monkeypatch.setattr("exercise_db.routers.programs.engine", test_engine)
    monkeypatch.setattr("exercise_db.routers.workouts.engine", test_engine)
    monkeypatch.setattr("exercise_db.routers.workout_templates.engine", test_engine)
    monkeypatch.setattr("exercise_db.routers.exercises.engine", test_engine)
    monkeypatch.setattr("exercise_db.routers.exercise_sets.engine", test_engine)
    monkeypatch.setattr("exercise_db.routers.workout_exercises.engine", test_engine)
    monkeypatch.setattr("exercise_db.routers.template_exercises.engine", test_engine)
    monkeypatch.setattr("exercise_db.routers.users.engine", test_engine)
    monkeypatch.setattr("exercise_db.routers.muscles.engine", test_engine)
    monkeypatch.setattr("exercise_db.routers.muscle_groups.engine", test_engine)
    monkeypatch.setattr("exercise_db.routers.program_types.engine", test_engine)

    client = TestClient(app)

    yield client

    test_engine.dispose()


@pytest.fixture(name="sample_program_type")
def sample_program_type_fixture(client):
    """Create a sample program type for testing."""
    from exercise_db.models.models import ProgramType
    from exercise_db.shared.utils import database

    with Session(database.engine) as session:
        program_type = ProgramType(name="Upper/Lower")
        session.add(program_type)
        session.commit()
        session.refresh(program_type)
        session.expunge(program_type)
        return program_type


@pytest.fixture(name="sample_program")
def sample_program_fixture(client, sample_program_type):
    """Create a sample program for testing."""
    from exercise_db.models.models import Program
    from exercise_db.shared.utils import database

    with Session(database.engine) as session:
        program = Program(
            name="Test Program",
            start_date=date(2024, 1, 1),
            description="A test program",
            program_type_id=sample_program_type.id,
        )
        session.add(program)
        session.commit()
        session.refresh(program)
        session.expunge(program)
        return program


@pytest.fixture(name="sample_muscle_group")
def sample_muscle_group_fixture(client):
    from exercise_db.models.models import MuscleGroup
    from exercise_db.shared.utils import database

    with Session(database.engine) as session:
        group = MuscleGroup(name="Chest")
        session.add(group)
        session.commit()
        session.refresh(group)
        session.expunge(group)
        return group


@pytest.fixture(name="sample_muscle")
def sample_muscle_fixture(client, sample_muscle_group):
    from exercise_db.models.models import Muscle
    from exercise_db.shared.utils import database

    with Session(database.engine) as session:
        muscle = Muscle(name="Pectoralis", muscle_group_id=sample_muscle_group.id)
        session.add(muscle)
        session.commit()
        session.refresh(muscle)
        session.expunge(muscle)
        return muscle


@pytest.fixture(name="sample_exercise")
def sample_exercise_fixture(client, sample_muscle):
    from exercise_db.models.models import Exercise
    from exercise_db.shared.utils import database

    with Session(database.engine) as session:
        exercise = Exercise(
            name="Bench Press",
            is_compound=True,
            muscle_primary=sample_muscle.id,
            muscle_secondary=sample_muscle.id,
        )
        session.add(exercise)
        session.commit()
        session.refresh(exercise)
        session.expunge(exercise)
        return exercise


@pytest.fixture(name="sample_workout_template")
def sample_workout_template_fixture(client, sample_program):
    from exercise_db.models.models import WorkoutTemplate
    from exercise_db.shared.utils import database

    with Session(database.engine) as session:
        template = WorkoutTemplate(day_of_week=1, label="Day 1", program_id=sample_program.id)
        session.add(template)
        session.commit()
        session.refresh(template)
        session.expunge(template)
        return template


@pytest.fixture(name="sample_template_exercise")
def sample_template_exercise_fixture(client, sample_workout_template, sample_exercise):
    from exercise_db.models.models import TemplateExercise
    from exercise_db.shared.utils import database

    with Session(database.engine) as session:
        template_exercise = TemplateExercise(
            order=1,
            workout_template_id=sample_workout_template.id,
            exercise_id=sample_exercise.id,
        )
        session.add(template_exercise)
        session.commit()
        session.refresh(template_exercise)
        session.expunge(template_exercise)
        return template_exercise


@pytest.fixture(name="sample_workout")
def sample_workout_fixture(client, sample_program, sample_workout_template):
    from exercise_db.models.models import Workout
    from exercise_db.shared.utils import database

    with Session(database.engine) as session:
        workout = Workout(
            program_id=sample_program.id,
            template_id=sample_workout_template.id,
            date=date(2024, 1, 10),
            duration=60,
        )
        session.add(workout)
        session.commit()
        session.refresh(workout)
        session.expunge(workout)
        return workout


@pytest.fixture(name="sample_workout_exercise")
def sample_workout_exercise_fixture(client, sample_workout, sample_exercise):
    from exercise_db.models.models import WorkoutExercise
    from exercise_db.shared.utils import database

    with Session(database.engine) as session:
        workout_exercise = WorkoutExercise(
            order=1,
            notes="Top set first",
            workout_id=sample_workout.id,
            exercise_id=sample_exercise.id,
        )
        session.add(workout_exercise)
        session.commit()
        session.refresh(workout_exercise)
        session.expunge(workout_exercise)
        return workout_exercise


@pytest.fixture(name="sample_exercise_set")
def sample_exercise_set_fixture(client, sample_workout_exercise):
    from exercise_db.models.models import ExerciseSet
    from exercise_db.shared.utils import database

    with Session(database.engine) as session:
        exercise_set = ExerciseSet(
            set_number=1,
            weight=135,
            reps=8,
            workout_exercise_id=sample_workout_exercise.id,
        )
        session.add(exercise_set)
        session.commit()
        session.refresh(exercise_set)
        session.expunge(exercise_set)
        return exercise_set


@pytest.fixture(name="sample_user")
def sample_user_fixture(client):
    from exercise_db.models.models import User
    from exercise_db.shared.utils import database

    with Session(database.engine) as session:
        user = User(
            user_name="jdoe",
            last_name="Doe",
            first_name="Jane",
            email="jane@example.com",
            creation_date=datetime(2024, 1, 1, 8, 0, 0),
            last_login_date=datetime(2024, 1, 2, 8, 0, 0),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        session.expunge(user)
        return user

