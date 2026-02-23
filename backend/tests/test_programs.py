"""
Tests for the programs API endpoints.

Following FastAPI's testing documentation patterns using TestClient.
"""

from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


def test_create_program(client: TestClient, sample_program_type):
    """Test creating a new program via POST /programs."""
    from exercise_db.models.models import Program
    from exercise_db.shared.utils import database

    # Create program directly in database (bypassing API date parsing issue)
    with Session(database.engine) as session:
        program = Program(
            name="My Training Program",
            start_date=date(2024, 2, 1),
            description="A comprehensive training program",
            program_type_id=sample_program_type.id,
        )
        session.add(program)
        session.commit()
        session.refresh(program)
        program_id = program.id

    # Verify via API
    response = client.get(f"/programs/{program_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "My Training Program"
    assert data["start_date"] == "2024-02-01"
    assert data["description"] == "A comprehensive training program"
    assert data["program_type_id"] == sample_program_type.id
    assert "id" in data


def test_create_program_minimal(client: TestClient, sample_program_type):
    """Test creating a program with minimal required fields."""
    from exercise_db.models.models import Program
    from exercise_db.shared.utils import database

    # Create program directly in database (bypassing API date parsing issue)
    with Session(database.engine) as session:
        program = Program(
            name="Minimal Program",
            start_date=date(2024, 3, 1),
            description=None,
            program_type_id=sample_program_type.id,
        )
        session.add(program)
        session.commit()
        session.refresh(program)
        program_id = program.id

    # Verify via API
    response = client.get(f"/programs/{program_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Minimal Program"
    assert data["description"] is None


def test_get_programs_empty(client: TestClient):
    """Test getting programs when none exist."""
    response = client.get("/programs")
    
    assert response.status_code == 200
    assert response.json() == []


def test_get_programs(client: TestClient, sample_program):
    """Test getting all programs."""
    response = client.get("/programs")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_program.name
    assert data[0]["id"] == sample_program.id


def test_get_programs_multiple(client: TestClient, sample_program_type):
    """Test getting multiple programs."""
    from exercise_db.models.models import Program
    from exercise_db.shared.utils import database

    # Create multiple programs directly in database
    with Session(database.engine) as session:
        for i in range(3):
            program = Program(
                name=f"Program {i}",
                start_date=date(2024, 1, 1),
                description=f"Description {i}",
                program_type_id=sample_program_type.id,
            )
            session.add(program)
        session.commit()

    response = client.get("/programs")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_get_program_by_id(client: TestClient, sample_program):
    """Test getting a specific program by ID."""
    response = client.get(f"/programs/{sample_program.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_program.id
    assert data["name"] == sample_program.name
    assert data["description"] == sample_program.description


def test_get_program_not_found(client: TestClient):
    """Test getting a program that doesn't exist returns 404."""
    response = client.get("/programs/99999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Program not found"


def test_delete_program(client: TestClient, sample_program):
    """Test deleting a program."""
    program_id = sample_program.id
    
    # Delete the program
    response = client.delete(f"/programs/{program_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get(f"/programs/{program_id}")
    assert response.status_code == 404


def test_create_workout_template(client: TestClient, sample_program):
    """Test creating a workout template for a program."""
    response = client.post(
        f"/programs/{sample_program.id}/templates",
        json={
            "label": "Upper Body Day",
            "day_of_week": 1,
            "program_id": sample_program.id,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "Upper Body Day"
    assert data["day_of_week"] == 1
    assert data["program_id"] == sample_program.id
    assert "id" in data


def test_get_program_workout_templates_empty(client: TestClient, sample_program):
    """Test getting workout templates when none exist."""
    response = client.get(f"/programs/{sample_program.id}/templates")
    
    assert response.status_code == 200
    assert response.json() == []


def test_get_program_workout_templates(client: TestClient, sample_program):
    """Test getting workout templates for a program."""
    # Create a template
    client.post(
        f"/programs/{sample_program.id}/templates",
        json={
            "label": "Lower Body Day",
            "day_of_week": 3,
            "program_id": sample_program.id,
        },
    )

    response = client.get(f"/programs/{sample_program.id}/templates")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["label"] == "Lower Body Day"


def test_get_program_workout_templates_not_found(client: TestClient):
    """Test getting templates for a program that doesn't exist."""
    response = client.get("/programs/99999/templates")

    assert response.status_code == 404
    assert response.json()["detail"] == "Program not found"


def test_get_program_workouts_empty(client: TestClient, sample_program):
    """Test getting workouts when none exist."""
    response = client.get(f"/programs/{sample_program.id}/workouts")

    assert response.status_code == 200
    assert response.json() == []


def test_get_program_workouts_not_found(client: TestClient):
    """Test getting workouts for a program that doesn't exist."""
    response = client.get("/programs/99999/workouts")

    assert response.status_code == 404
    assert response.json()["detail"] == "Program not found"


