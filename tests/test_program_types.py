from datetime import date

from sqlmodel import Session


def test_create_program_type(client):
    response = client.post("/program_types", json={"name": "Push/Pull"})

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Push/Pull"
    assert "id" in data


def test_get_program_types(client, sample_program_type):
    response = client.get("/program_types")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_program_type.id


def test_get_program_type_by_id(client, sample_program_type):
    response = client.get(f"/program_types/{sample_program_type.id}")

    assert response.status_code == 200
    assert response.json()["name"] == sample_program_type.name


def test_get_program_type_not_found(client):
    response = client.get("/program_types/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Program type not found"


def test_delete_program_type(client, sample_program_type):
    response = client.delete(f"/program_types/{sample_program_type.id}")
    assert response.status_code == 204

    response = client.get(f"/program_types/{sample_program_type.id}")
    assert response.status_code == 404


def test_get_programs_by_program_type(client, sample_program_type):
    from models.models import Program
    from shared.utils import database

    with Session(database.engine) as session:
        program = Program(
            name="Program A",
            start_date=date(2024, 1, 1),
            description="desc",
            program_type_id=sample_program_type.id,
        )
        session.add(program)
        session.commit()

    response = client.get(f"/program_types/{sample_program_type.id}/programs")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Program A"


def test_get_programs_by_program_type_not_found(client):
    response = client.get("/program_types/99999/programs")

    assert response.status_code == 404
    assert response.json()["detail"] == "Program type not found"
