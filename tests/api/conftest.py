from fastapi.testclient import TestClient
from pytest import fixture

from back.db.models import User


def auth_user(client: TestClient, user: User) -> TestClient:
    response = client.post(
        "/auth/token",
        data={"username": user.username, "password": user.username},
    )
    assert response.status_code == 200

    data = response.json()
    access_token = data["access_token"]
    token_type = data["token_type"]

    client.headers = {"Authorization": f"{token_type} {access_token}"}
    return client


@fixture
def client1(users, client) -> TestClient:
    return auth_user(client, users[0])


@fixture
def client2(users, client) -> TestClient:
    return auth_user(client, users[1])
