def test_create_muscle(client, sample_muscle_group):
    response = client.post(
        "/muscles",
        json={"name": "Quadriceps", "muscle_group_id": sample_muscle_group.id},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Quadriceps"
    assert data["muscle_group_id"] == sample_muscle_group.id


def test_get_muscles(client, sample_muscle):
    response = client.get("/muscles")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_muscle.id


def test_get_muscles_filter_by_group_name(client, sample_muscle_group, sample_muscle):
    response = client.get(f"/muscles?muscle_group={sample_muscle_group.name}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_muscle.name


def test_get_muscle_by_id(client, sample_muscle):
    response = client.get(f"/muscles/{sample_muscle.id}")

    assert response.status_code == 200
    assert response.json()["id"] == sample_muscle.id


def test_get_muscle_not_found(client):
    response = client.get("/muscles/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Muscle not found"


def test_delete_muscle(client, sample_muscle):
    response = client.delete(f"/muscles/{sample_muscle.id}")
    assert response.status_code == 204

    response = client.get(f"/muscles/{sample_muscle.id}")
    assert response.status_code == 404
