def test_get_exercise_set(client, sample_exercise_set):
    response = client.get(f"/exercise_sets/{sample_exercise_set.id}")

    assert response.status_code == 200
    assert response.json()["id"] == sample_exercise_set.id


def test_get_exercise_set_not_found(client):
    response = client.get("/exercise_sets/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Exercise set not found"


def test_update_exercise_set(client, sample_exercise_set, sample_workout_exercise):
    response = client.put(
        f"/exercise_sets/{sample_exercise_set.id}",
        json={
            "id": sample_exercise_set.id,
            "set_number": 2,
            "weight": 155,
            "reps": 10,
            "workout_exercise_id": sample_workout_exercise.id,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["set_number"] == 2
    assert data["weight"] == 155
    assert data["reps"] == 10


def test_delete_exercise_set(client, sample_exercise_set):
    response = client.delete(f"/exercise_sets/{sample_exercise_set.id}")
    assert response.status_code == 204

    response = client.get(f"/exercise_sets/{sample_exercise_set.id}")
    assert response.status_code == 404
