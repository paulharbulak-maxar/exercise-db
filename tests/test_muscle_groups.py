def test_create_muscle_group(client):
    response = client.post("/muscle_groups", json={"name": "Legs"})

    assert response.status_code == 200
    assert response.json()["name"] == "Legs"


def test_get_muscle_groups(client, sample_muscle_group):
    response = client.get("/muscle_groups")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_muscle_group.id


def test_get_muscle_group_by_id(client, sample_muscle_group):
    response = client.get(f"/muscle_groups/{sample_muscle_group.id}")

    assert response.status_code == 200
    assert response.json()["name"] == sample_muscle_group.name


def test_get_muscle_group_not_found(client):
    response = client.get("/muscle_groups/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Muscle group not found"


def test_delete_muscle_group(client, sample_muscle_group):
    response = client.delete(f"/muscle_groups/{sample_muscle_group.id}")
    assert response.status_code == 204

    response = client.get(f"/muscle_groups/{sample_muscle_group.id}")
    assert response.status_code == 404


def test_get_muscles_by_muscle_group(client, sample_muscle_group, sample_muscle):
    response = client.get(f"/muscle_groups/{sample_muscle_group.id}/muscles")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_muscle.id


def test_get_muscles_by_muscle_group_not_found(client):
    response = client.get("/muscle_groups/99999/muscles")

    assert response.status_code == 404
    assert response.json()["detail"] == "Muscle group not found"
