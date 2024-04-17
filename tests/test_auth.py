def test_login(users, client):
    response = client.post(
        "/auth/token",
        data={"username": users[0].username, "password": "wrong_password"},
    )
    assert response.status_code == 401

    response = client.post(
        "/auth/token",
        data={"username": users[0].username, "password": users[0].username},
    )
    assert response.status_code == 200


def test_register(client):
    username, password = "aboba", "aboba123"

    response = client.post(
        "/auth/token", data={"username": username, "password": password}
    )
    assert response.status_code == 401

    response = client.post(
        "/auth/register", json={"username": username, "password": password}
    )
    assert response.status_code == 200

    response = client.post(
        "/auth/token", data={"username": username, "password": password}
    )
    assert response.status_code == 200
