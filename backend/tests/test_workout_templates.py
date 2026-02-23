from datetime import date


def test_get_workout_template(client, sample_workout_template):
    response = client.get(f"/workout_templates/{sample_workout_template.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_workout_template.id
    assert data["program_id"] == sample_workout_template.program_id


def test_get_workout_template_not_found(client):
    response = client.get("/workout_templates/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Workout template not found"


def test_update_workout_template(client, sample_workout_template):
    response = client.put(
        f"/workout_templates/{sample_workout_template.id}",
        json={
            "id": sample_workout_template.id,
            "day_of_week": 2,
            "label": "Updated Label",
            "program_id": sample_workout_template.program_id,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["day_of_week"] == 2
    assert data["label"] == "Updated Label"


def test_create_template_exercise_on_workout_template(client, sample_workout_template, sample_exercise):
    response = client.post(
        f"/workout_templates/{sample_workout_template.id}/template_exercises",
        json={
            "order": 1,
            "workout_template_id": sample_workout_template.id,
            "exercise_id": sample_exercise.id,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["workout_template_id"] == sample_workout_template.id
    assert data["exercise_id"] == sample_exercise.id


def test_get_workout_template_exercises(client, sample_template_exercise, sample_workout_template):
    response = client.get(f"/workout_templates/{sample_workout_template.id}/exercises")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_template_exercise.id


def test_create_workout_from_template_creates_exercises(
    client, sample_program, sample_workout_template, sample_template_exercise
):
    response = client.post(
        f"/workout_templates/{sample_workout_template.id}/workouts",
        json={
            "program_id": sample_program.id,
            "template_id": sample_workout_template.id,
            "date": date(2024, 1, 20).isoformat(),
            "duration": 45,
        },
    )

    assert response.status_code == 200
    workout_data = response.json()

    exercises_response = client.get(f"/workouts/{workout_data['id']}/exercises")
    assert exercises_response.status_code == 200
    exercises_data = exercises_response.json()
    assert len(exercises_data) == 1
    assert exercises_data[0]["exercise_id"] == sample_template_exercise.exercise_id


def test_delete_workout_template(client, sample_workout_template):
    response = client.delete(f"/workout_templates/{sample_workout_template.id}")
    assert response.status_code == 204

    response = client.get(f"/workout_templates/{sample_workout_template.id}")
    assert response.status_code == 404

