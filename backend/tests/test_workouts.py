from datetime import date


def test_create_workout(client, sample_program, sample_workout_template):
    response = client.post(
        "/workouts",
        json={
            "program_id": sample_program.id,
            "template_id": sample_workout_template.id,
            "date": date(2024, 2, 1).isoformat(),
            "duration": 60,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["program_id"] == sample_program.id
    assert data["template_id"] == sample_workout_template.id


def test_update_workout(client, sample_workout):
    response = client.put(
        f"/workouts/{sample_workout.id}",
        json={
            "id": sample_workout.id,
            "program_id": sample_workout.program_id,
            "template_id": sample_workout.template_id,
            "date": sample_workout.date.isoformat(),
            "duration": 75,
        },
    )

    assert response.status_code == 200
    assert response.json()["duration"] == 75


def test_get_workouts(client, sample_workout):
    response = client.get("/workouts")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_workout.id


def test_get_workout_by_id(client, sample_workout):
    response = client.get(f"/workouts/{sample_workout.id}")

    assert response.status_code == 200
    assert response.json()["id"] == sample_workout.id


def test_get_workout_not_found(client):
    response = client.get("/workouts/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Workout not found"


def test_delete_workout(client, sample_workout):
    response = client.delete(f"/workouts/{sample_workout.id}")
    assert response.status_code == 204

    response = client.get(f"/workouts/{sample_workout.id}")
    assert response.status_code == 404


def test_create_workout_exercise(client, sample_workout, sample_exercise):
    response = client.post(
        f"/workouts/{sample_workout.id}/workout_exercises",
        json={
            "order": 1,
            "notes": "Warm-up then top set",
            "workout_id": sample_workout.id,
            "exercise_id": sample_exercise.id,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["workout_id"] == sample_workout.id
    assert data["exercise_id"] == sample_exercise.id


def test_get_workout_exercises(client, sample_workout_exercise, sample_workout):
    response = client.get(f"/workouts/{sample_workout.id}/exercises")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_workout_exercise.id

