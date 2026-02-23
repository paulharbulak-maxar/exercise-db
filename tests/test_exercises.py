from sqlmodel import Session


def test_create_exercise(client, sample_muscle):
    response = client.post(
        "/exercises",
        json={
            "name": "Incline Bench Press",
            "is_compound": True,
            "muscle_primary": sample_muscle.id,
            "muscle_secondary": sample_muscle.id,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Incline Bench Press"
    assert data["muscle_primary"] == sample_muscle.id


def test_get_exercises(client, sample_exercise):
    response = client.get("/exercises")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_exercise.id


def test_get_exercises_filter_by_muscle(client, sample_muscle, sample_exercise):
    response = client.get(f"/exercises?muscle={sample_muscle.name}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_exercise.name


def test_get_exercises_filter_by_muscle_group(client, sample_muscle_group, sample_exercise):
    response = client.get(f"/exercises?muscle_group={sample_muscle_group.name}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_exercise.name


def test_get_exercise_by_id(client, sample_exercise):
    response = client.get(f"/exercises/{sample_exercise.id}")

    assert response.status_code == 200
    assert response.json()["id"] == sample_exercise.id


def test_get_exercise_not_found(client):
    response = client.get("/exercises/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Exercise not found"


def test_delete_exercise(client, sample_exercise):
    response = client.delete(f"/exercises/{sample_exercise.id}")
    assert response.status_code == 204

    response = client.get(f"/exercises/{sample_exercise.id}")
    assert response.status_code == 404
