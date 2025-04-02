from .database import client, session
from app import schemas


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello@gmail.com", "password": "abc123"}
    )

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201

def test_login_user(client):
    res = client.post(
        "/login", data={"username": "hello@gmail.com", "password": "abc123"}
    )

    assert res.status_code == 200
