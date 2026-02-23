def test_get_workout_exercise(client, sample_workout_exercise):
    response = client.get(f"/workout_exercises/{sample_workout_exercise.id}")

    assert response.status_code == 200
    assert response.json()["id"] == sample_workout_exercise.id


def test_get_workout_exercise_not_found(client):
    response = client.get("/workout_exercises/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Workout exercise not found"


def test_update_workout_exercise(client, sample_workout_exercise, sample_workout, sample_exercise):
    response = client.put(
        f"/workout_exercises/{sample_workout_exercise.id}",
        json={
            "id": sample_workout_exercise.id,
            "order": 1,
            "notes": "Updated notes",
            "workout_id": sample_workout.id,
            "exercise_id": sample_exercise.id,
        },
    )

    assert response.status_code == 200
    assert response.json()["notes"] == "Updated notes"


def test_delete_workout_exercise(client, sample_workout_exercise):
    response = client.delete(f"/workout_exercises/{sample_workout_exercise.id}")
    assert response.status_code == 204

    response = client.get(f"/workout_exercises/{sample_workout_exercise.id}")
    assert response.status_code == 404


def test_create_and_get_workout_exercise_sets(client, sample_workout_exercise):
    create_response = client.post(
        f"/workout_exercises/{sample_workout_exercise.id}/exercise_sets",
        json={
            "set_number": 1,
            "weight": 185,
            "reps": 5,
            "workout_exercise_id": sample_workout_exercise.id,
        },
    )
    assert create_response.status_code == 200

    get_response = client.get(f"/workout_exercises/{sample_workout_exercise.id}/exercise_sets")
    assert get_response.status_code == 200
    data = get_response.json()
    assert len(data) == 1
    assert data[0]["weight"] == 185


def test_create_workout_exercise_set_not_found(client):
    response = client.post(
        "/workout_exercises/99999/exercise_sets",
        json={"set_number": 1, "weight": 100, "reps": 8, "workout_exercise_id": 99999},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Workout exercise not found"
