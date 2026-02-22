"""
Test configuration and fixtures for the exercise-db test suite.

This module provides pytest fixtures for database setup and FastAPI TestClient
following the patterns from FastAPI's official documentation.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app

# Import all models to ensure they're registered with SQLModel metadata
from models.models import (  # noqa: F401
    Program,
    ProgramType,
    User,
    MuscleGroup,
    Muscle,
    Exercise,
    EmgActivation,
    TemplateExercise,
    WorkoutTemplate,
    Workout,
    WorkoutExercise,
    ExerciseSet,
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
    # Create test engine
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    SQLModel.metadata.create_all(test_engine)

    # Patch the engine in the database module and all routers that import it
    monkeypatch.setattr("shared.utils.database.engine", test_engine)
    monkeypatch.setattr("routers.programs.engine", test_engine)
    monkeypatch.setattr("routers.workouts.engine", test_engine)
    monkeypatch.setattr("routers.workout_templates.engine", test_engine)
    monkeypatch.setattr("routers.exercises.engine", test_engine)
    monkeypatch.setattr("routers.exercise_sets.engine", test_engine)
    monkeypatch.setattr("routers.workout_exercises.engine", test_engine)
    monkeypatch.setattr("routers.template_exercises.engine", test_engine)
    monkeypatch.setattr("routers.users.engine", test_engine)
    monkeypatch.setattr("routers.muscles.engine", test_engine)
    monkeypatch.setattr("routers.muscle_groups.engine", test_engine)
    monkeypatch.setattr("routers.program_types.engine", test_engine)

    # Create client
    client = TestClient(app)

    yield client

    # Close test engine
    test_engine.dispose()


@pytest.fixture(name="sample_program_type")
def sample_program_type_fixture(client):
    """Create a sample program type for testing."""
    from shared.utils import database
    from models.models import ProgramType

    with Session(database.engine) as session:
        program_type = ProgramType(name="Upper/Lower")
        session.add(program_type)
        session.commit()
        session.refresh(program_type)
        # Detach from session so it can be used across requests
        session.expunge(program_type)
        return program_type


@pytest.fixture(name="sample_program")
def sample_program_fixture(client, sample_program_type):
    """Create a sample program for testing."""
    from datetime import date
    from shared.utils import database
    from models.models import Program

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
        # Detach from session so it can be used across requests
        session.expunge(program)
        return program

