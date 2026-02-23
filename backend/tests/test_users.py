from datetime import datetime


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "user_name": "asmith",
            "last_name": "Smith",
            "first_name": "Alex",
            "email": "alex@example.com",
            "creation_date": datetime(2024, 1, 1, 10, 0, 0).isoformat(),
            "last_login_date": datetime(2024, 1, 2, 10, 0, 0).isoformat(),
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["user_name"] == "asmith"
    assert data["email"] == "alex@example.com"


def test_get_users(client, sample_user):
    response = client.get("/users")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_user.id
    assert data[0]["user_name"] == sample_user.user_name

