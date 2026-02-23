from sqlmodel import Session


def test_create_template_exercise(client, sample_workout_template, sample_exercise):
    response = client.post(
        "/template_exercises",
        json={
            "order": 1,
            "workout_template_id": sample_workout_template.id,
            "exercise_id": sample_exercise.id,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["order"] == 1
    assert data["exercise_id"] == sample_exercise.id


def test_get_template_exercise(client, sample_template_exercise):
    response = client.get(f"/template_exercises/{sample_template_exercise.id}")

    assert response.status_code == 200
    assert response.json()["id"] == sample_template_exercise.id


def test_get_template_exercise_not_found(client):
    response = client.get("/template_exercises/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Template exercise not found"


def test_update_template_exercise_order(client, sample_workout_template, sample_exercise):
    from models.models import TemplateExercise
    from shared.utils import database

    with Session(database.engine) as session:
        first = TemplateExercise(
            order=1,
            workout_template_id=sample_workout_template.id,
            exercise_id=sample_exercise.id,
        )
        second = TemplateExercise(
            order=2,
            workout_template_id=sample_workout_template.id,
            exercise_id=sample_exercise.id,
        )
        session.add(first)
        session.add(second)
        session.commit()
        session.refresh(second)

        second_id = second.id
        first_id = first.id

    response = client.put(f"/template_exercises/{second_id}?order=1")

    assert response.status_code == 200
    assert response.json()["order"] == 1

    response_first = client.get(f"/template_exercises/{first_id}")
    assert response_first.status_code == 200
    assert response_first.json()["order"] == 2


def test_delete_template_exercise(client, sample_template_exercise):
    response = client.delete(f"/template_exercises/{sample_template_exercise.id}")
    assert response.status_code == 204

    response = client.get(f"/template_exercises/{sample_template_exercise.id}")
    assert response.status_code == 404
